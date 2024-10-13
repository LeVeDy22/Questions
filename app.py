import requests as rq
import flet as ft
import html
import sys
import os
import subprocess


def fetch_data():
    try:
        response = rq.get(
            "https://opentdb.com/api.php?amount=10&difficulty=easy&type=boolean"
        )
        if response.status_code != 200:
            return {"question": "Error: Failed to retrieve data."}

        data = response.json()
        if "results" not in data or len(data["results"]) == 0:
            return {"question": "Error: Invalid data structure."}

        result = data["results"][0]
        return result

    except Exception as e:
        return {"question": f"Error executing the request: {str(e)}"}


def main(page: ft.Page):
    page.title = "Flet Questions"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.theme_mode = "dark"

    result = fetch_data()

    def restart_app(e):
        page.window_close()
        python = sys.executable
        subprocess.Popen([python] + sys.argv)
        os._exit(0)

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    def check_answer(e, user_answer):
        correct_answer = result["correct_answer"]
        if user_answer == correct_answer:
            answer.value = "Correct!"
        else:
            answer.value = "Incorrect("
        page.update()

    question = ft.Text(html.unescape(result["question"]))
    answer = ft.Text()

    theme_button = ft.IconButton(icon=ft.icons.SUNNY, on_click=change_theme)
    true_button = ft.ElevatedButton("True", on_click=lambda e: check_answer(e, "True"))
    false_button = ft.ElevatedButton(
        "False", on_click=lambda e: check_answer(e, "False")
    )
    restart_button = ft.ElevatedButton("Restart", on_click=restart_app)

    Row_TrueFalse = ft.Row(
        [
            true_button,
            false_button,
        ],
        alignment="center",
        vertical_alignment="center",
    )

    page.add(
        ft.Column(
            [
                ft.Column(
                    [
                        theme_button,
                        question,
                        Row_TrueFalse,
                        answer,
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                    expand=True,
                ),
                ft.Container(
                    restart_button,
                    alignment=ft.alignment.center,
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True,
        )
    )


ft.app(target=main)
