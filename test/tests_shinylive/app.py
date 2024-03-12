import test_pyfetch as tests
from shiny import App, Inputs, Outputs, Session, reactive, ui

app_ui = ui.page_fluid(
    ui.input_action_button("tests_btn", "Run tests")
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.effect
    @reactive.event(input.tests_btn)
    async def all_tests():
        test_l = [
            tests.test_wrapper_get_string,
            tests.test_wrapper_get_json,
             tests.test_wrapper_get_parameter_found,
             tests.test_wrapper_get_parameter_not_found,
             tests.test_wrapper_post_payload,
             tests.test_wrapper_get_file_download,
             tests.test_wrapper_get_image_download,
             tests.test_wrapper_streaming_fake,
        ]
        for t in test_l:
            print(f"Running {t.__name__}...", end="")
            await t()
            print(" ...passed")

app = App(app_ui, server)
