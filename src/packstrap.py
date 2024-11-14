import gradio as gr


class PackStrap():

    def head_strap(platform, local=False):
        if local:
            if platform == "iOS":
                return head_ios
            if platform == "Android":
                return head_droid
        else:
            return head_remote
        

    # TODO: Provide a UUID for future tracking
    head_remote = f"""
    <script src="https://baseweight.ai/daypack/daypack.js">
    """

    head_ios = f"""
    <script src="daypack.js">
    """

    head_droid = f"""
    <script src="file:/android_assets/daypack/daypack.js">
    """

        