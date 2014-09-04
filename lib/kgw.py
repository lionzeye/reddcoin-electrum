__author__ = 'laudney'


from pprint import pprint


# Kimoto Gravity Well difficulty retarget algo for Reddcoin
class KGW(object):
    def __init__(self):
        self.target_block_spacing_seconds = 60
        self.time_day_seconds = 24 * 60 * 60
        self.last_pow_block = 260799

        # 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        self.max_target = 2**236 - 1
        self.max_nbits = 0x1e0fffff
        self.min_difficulty = 0xFFFF / (2**28 - 1.0 / 2**208)

        self.genesis_target = 0x00000FFFF0000000000000000000000000000000000000000000000000000000
        self.genesis_nbits = 0x1e0ffff0

        self.posv_reset_target = 2**224 - 1
        self.posv_reset_difficulty = 0xFFFF / (2**16 - 1.0 / 2**208)
        self.posv_reset_nbits = 0x1d00ffff

    def past_blocks(self, next_height):
        if next_height <= 6000:
            past_seconds_min = int(self.time_day_seconds * 0.01)
            past_seconds_max = int(self.time_day_seconds * 0.14)
        else:
            past_seconds_min = self.time_day_seconds / 4
            past_seconds_max = self.time_day_seconds * 7

        past_blocks_min = past_seconds_min / self.target_block_spacing_seconds
        past_blocks_max = past_seconds_max / self.target_block_spacing_seconds

        return past_blocks_min, past_blocks_max

    def target2nbits(self, target):
        target = int(target)
        MM = 256 * 256 * 256
        c = ("%064X" % target)[2:]
        i = 31
        while c[0:2] == "00":
            c = c[2:]
            i -= 1

        c = int('0x' + c[0:6], 16)
        if c >= 0x800000:
            c /= 256
            i += 1

        return c + MM * i

    def nbits2target(self, nbits):
        nbits = int(nbits)
        MM = 256 * 256 * 256
        a = nbits % MM
        if a < 0x8000:
            a *= 256

        return a * pow(2, 8 * (nbits / MM - 3))

    def get_target(self, chain=None):
        if chain is None or len(chain) == 0:
            return self.genesis_nbits, self.genesis_target

        first_block = chain[0]
        last_block = chain[-1]
        last_timestamp = int(last_block.get('timestamp'))
        first_height = max(0, first_block.get('block_height') - 1)
        last_height = last_block.get('block_height')
        next_height = last_height + 1

        past_blocks_min, past_blocks_max = self.past_blocks(next_height)

        is_posv = last_height >= self.last_pow_block

        if is_posv:
            first_height = self.last_pow_block

        if last_height < past_blocks_min:
            return self.max_nbits, self.max_target

        if is_posv and (last_height - self.last_pow_block) < past_blocks_min:
            return self.posv_reset_nbits, self.posv_reset_target

        past_blocks_mass = past_rate_actual_seconds = past_rate_target_seconds = 0
        past_target_average = past_target_average_prev = None
        height_reading = last_height

        i = 1
        while height_reading > first_height:
            if i > past_blocks_max:
                break

            past_blocks_mass += 1
            block_reading = chain[-i]
            timestamp_reading = int(block_reading.get('timestamp'))
            target_reading = self.nbits2target(block_reading.get('bits'))

            if i == 1:
                past_target_average = float(target_reading)
            else:
                past_target_average = (target_reading - past_target_average_prev) / float(i) + past_target_average_prev

            past_target_average_prev = past_target_average

            past_rate_actual_seconds = max(0, last_timestamp - timestamp_reading)
            past_rate_target_seconds = self.target_block_spacing_seconds * past_blocks_mass
            past_rate_adjustment_ratio = 1.0
            if past_rate_actual_seconds != 0 and past_rate_target_seconds != 0:
                past_rate_adjustment_ratio = float(past_rate_target_seconds) / float(past_rate_actual_seconds)

            event_horizon_deviation = 1 + (0.7084 * pow(past_blocks_mass / 144.0, -1.228))
            event_horizon_deviation_fast = event_horizon_deviation
            event_horizon_deviation_slow = 1 / event_horizon_deviation

            if past_blocks_mass >= past_blocks_min:
                if past_rate_adjustment_ratio <= event_horizon_deviation_slow or \
                        past_rate_adjustment_ratio >= event_horizon_deviation_fast:
                    break

            height_reading -= 1
            i += 1

        # failed to calculate difficulty due to not enough blocks
        if height_reading <= first_height:
            return None, None

        new_target = past_target_average
        if past_rate_actual_seconds != 0 and past_rate_target_seconds != 0:
            new_target *= past_rate_actual_seconds
            new_target /= past_rate_target_seconds

        new_target = min(int(new_target), self.max_target)
        new_nbits = self.target2nbits(new_target)
        return new_nbits, new_target

    def get_chain_target(self, prev_chain, chain):
        full_chain = prev_chain + chain
        return [self.get_target(full_chain[:i]) for i in range(len(prev_chain)+1, len(full_chain))]
