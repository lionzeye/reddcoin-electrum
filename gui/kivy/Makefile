PYTHON = python
# needs kivy installed or in PYTHONPATH

.PHONY: theming apk clean

theming:
	$(PYTHON) -m kivy.atlas theming/light 1024 theming/light/*.png
apk:
	# running pre build setup
	@cp tools/buildozer.spec ../../buildozer.spec
	# rename reddcoin-electrum to main.py
	@mv ../../reddcoin-electrum ../../main.py
	@-if [ ! -d "../../.buildozer" ];then \
		cd ../..; buildozer android debug;\
		cp -f gui/kivy/tools/blacklist.txt .buildozer/android/platform/python-for-android/src/blacklist.txt;\
		rm -rf ./.buildozer/android/platform/python-for-android/dist;\
	fi
	@-cd ../..; buildozer android debug deploy run
	@make clean
clean:
	# Cleaning up
	# rename main.py to reddcoin-electrum
	@-mv ../../main.py ../../reddcoin-electrum
	# remove buildozer.spec
	@-rm ../../buildozer.spec
