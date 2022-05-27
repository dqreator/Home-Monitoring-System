# > Uncomment for garbage collector pythn output or debugging features
# import gc
# import ptvsd

from app import wardrobeuApp


if __name__ == "__main__":
    # > Uncomment to attach VSCode debugegr
    # print("Waiting for debugger attach")
    # ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
    # ptvsd.wait_for_attach()

    # > Uncomment to get garbage collector debug output
    # gc.set_debug(gc.DEBUG_STATS)
    # gc.set_debug(gc.DEBUG_LEAK)

    application = wardrobeuApp()
    application.run()