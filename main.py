import flet as ft
import random
import string
import pyperclip as pc
from password_strength import PasswordPolicy
import keyring as kr


def main(page: ft.Page):
    def Generate(e):
        if pass_length.value is None:
            exit()

        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        number = string.digits
        symbol = string.punctuation
        All = upper + lower + number + symbol

        temp = "".join(random.sample(All, int(pass_length.value)))
        gen_pass.value = temp
        page.update()

    def Copy(e):
        pc.copy(gen_pass.value)
        snack_bar_text.value = 'Copied to clipboard'
        page.snack_bar.open = True
        page.update()

    def Test(e):
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=2,
            numbers=2,
            special=2,
            nonletters=2,
        )
        if not pass_test.value:
            exit()

        test = policy.test(pass_test.value)
        if len(test) >= 2:
            weak.visible = True
            page.update()

        elif len(test) == 1:
            medium.visible = True
            page.update()

        elif len(test) == 0:
            strong.visible = True
            page.update()

    def Test_change(e):
        strong.visible = False
        medium.visible = False
        weak.visible = False
        page.update()

    def back(e):
        back_button.visible = False
        heading.value = None
        gen_pass.value = None
        pass_test.value = None
        Test_change(e)
        pass_length.value = None
        reset_border_colors()
        reset_fields_text()
        fetch_pass.visible = False
        delete_pass.visible = False
        add_pass.visible = False
        main_page.content = home_page
        page.update()

    def load_gen_page(e):
        back_button.visible = True
        heading.value = 'Generate Passwords'
        main_page.content = gen_page
        page.update()

    def load_save_page(e):
        back_button.visible = True
        heading.value = 'Save Passwords'
        main_page.content = save_page
        page.update()

    def load_test_page(e):
        back_button.visible = True
        heading.value = 'Test Password Strength'
        main_page.content = test_page
        page.update()

    def reset_border_colors():
        identifier_field_add.border_color = None
        identifier_field_fetch.border_color = None
        identifier_field_delete.border_color = None
        username_field_add.border_color = None
        username_field_fetch.border_color = None
        username_field_delete.border_color = None
        password_field.border_color = None
        confirm_password_field.border_color = None

    def reset_fields_text():
        identifier_field_add.value = None
        identifier_field_fetch.value = None
        identifier_field_delete.value = None
        username_field_add.value = None
        username_field_fetch.value = None
        username_field_delete.value = None
        password_field.value = None
        confirm_password_field.value = None

    def add_clicked(e):
        reset_border_colors()
        reset_fields_text()
        fetch_pass.visible = False
        delete_pass.visible = False
        add_pass.visible = True
        page.update()

    def delete_clicked(e):
        reset_border_colors()
        reset_fields_text()
        fetch_pass.visible = False
        delete_pass.visible = True
        add_pass.visible = False
        page.update()

    def fetch_clicked(e):
        reset_border_colors()
        reset_fields_text()
        fetch_pass.visible = True
        delete_pass.visible = False
        add_pass.visible = False
        page.update()

    def fetch(e):
        if identifier_field_fetch.value == '' or identifier_field_fetch.value.isspace():
            identifier_field_fetch.border_color = 'red'
        elif username_field_fetch.value == '' or username_field_fetch.value.isspace():
            username_field_fetch.border_color = 'red'
        else:
            fetch_result = kr.get_credential(
                service_name=identifier_field_fetch.value,
                username=username_field_fetch.value
            )
            if fetch_result is None:
                snack_bar_text.value = "Couldn't fetch credential"
                page.snack_bar.open = True
                reset_fields_text()
                page.update()
                exit()
            else:
                if fetch_result.username == username_field_fetch.value:
                    pc.copy(fetch_result.password)
                    snack_bar_text.value = "Copied to clipboard"
                    page.snack_bar.open = True
                    reset_fields_text()

        page.update()

    def delete_cred(e):
        if identifier_field_delete.value == '' or identifier_field_delete.value.isspace():
            identifier_field_delete.border_color = 'red'
        elif username_field_delete.value == '' or username_field_delete.value.isspace():
            username_field_delete.border_color = 'red'
        else:
            delete_result = kr.get_credential(
                service_name=identifier_field_delete.value,
                username=username_field_delete.value
            )
            if delete_result is None:
                snack_bar_text.value = "Couldn't delete credentials"
                page.snack_bar.open = True
                reset_fields_text()
                page.update()
                exit()
            else:
                if delete_result.username == username_field_delete.value:
                    kr.delete_password(
                        service_name=identifier_field_delete.value,
                        username=username_field_delete.value,
                    )
                    snack_bar_text.value = "Credential deleted"
                    page.snack_bar.open = True
                    reset_fields_text()

        page.update()

    def add_new(e):
        if identifier_field_add.value == '' or identifier_field_add.value.isspace():
            identifier_field_add.border_color = 'red'
        elif username_field_add.value == '' or username_field_add.value.isspace():
            username_field_add.border_color = 'red'
        elif password_field.value == '' or password_field.value.isspace():
            password_field.border_color = 'red'
        elif confirm_password_field.value == '' or confirm_password_field.value.isspace():
            confirm_password_field.border_color = 'red'
        else:
            if password_field.value == confirm_password_field.value:
                kr.set_password(
                    service_name=identifier_field_add.value,
                    username=username_field_add.value,
                    password=password_field.value
                )
                snack_bar_text.value = 'Credentials added successfully'
                page.snack_bar.open = True
                reset_fields_text()
            else:
                snack_bar_text.value = "Passwords Don't match"
                page.snack_bar.open = True
                password_field.border_color = 'red'
                confirm_password_field.border_color = 'red'
        page.update()

    def field_change(e):
        reset_border_colors()
        page.update()

    gen_pass = ft.Text(
        value=None,
        weight=ft.FontWeight.BOLD,
        size=16
    )

    pass_length = ft.Dropdown(
        width=100,
        label="length",
        options=[
            ft.dropdown.Option("8"),
            ft.dropdown.Option("10"),
            ft.dropdown.Option("12"),
            ft.dropdown.Option("14"),
        ],

    )

    pass_test = ft.TextField(label="Password", width=220, on_change=Test_change)
    heading = ft.Text(
        value=None, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87
    )
    snack_bar_text = ft.Text("")
    snack_bar_action = "Done"
    identifier_field_add = ft.TextField(
        label="Identifier", width=150,
        on_change=field_change, border_color='',
    )
    identifier_field_fetch = ft.TextField(
        label="Identifier", width=150,
        on_change=field_change, border_color='',
    )
    identifier_field_delete = ft.TextField(
        label="Identifier", width=150,
        on_change=field_change, border_color='',
    )
    username_field_add = ft.TextField(
        label="Username", width=150,
        on_change=field_change, border_color='',
    )
    username_field_fetch = ft.TextField(
        label="Username", width=150,
        on_change=field_change, border_color='',
    )
    username_field_delete = ft.TextField(
        label="Username", width=150,
        on_change=field_change, border_color='',
    )
    password_field = ft.TextField(
        label="Password", width=220, border_color='',
        on_change=field_change, password=True, can_reveal_password=True
    )
    confirm_password_field = ft.TextField(
        label="Confirm", width=220, border_color='',
        on_change=field_change, password=True, can_reveal_password=True
    )

    strong = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        offset=ft.Offset(-0.14, 0),
        controls=[
            ft.Icon(name=ft.icons.CHECK_CIRCLE_ROUNDED, color=ft.colors.GREEN),
            ft.Text("Strong")
        ],
        visible=False
    )

    medium = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        offset=ft.Offset(-0.14, 0),
        controls=[
            ft.Icon(name=ft.icons.DO_NOT_DISTURB_ON_SHARP, color=ft.colors.YELLOW_700),
            ft.Text("Medium")
        ],
        visible=False
    )

    weak = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        offset=ft.Offset(-0.14, 0),
        controls=[
            ft.Icon(name=ft.icons.ERROR, color=ft.colors.RED),
            ft.Text("Weak")
        ],
        visible=False
    )

    back_button = ft.IconButton(
        icon=ft.icons.ARROW_CIRCLE_LEFT,
        icon_size=30,
        icon_color=ft.colors.GREY,
        tooltip="Back",
        visible=False,
        on_click=back
    )

    gen_button = ft.Container(
        width=150,
        height=150,
        border_radius=20,
        bgcolor=ft.colors.SURFACE_VARIANT,
        alignment=ft.alignment.center,
        on_click=load_gen_page,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(name=ft.icons.MISCELLANEOUS_SERVICES_ROUNDED, size=48),
                ft.Text(value='Generate', weight=ft.FontWeight.BOLD)
            ]
        )
    )

    store_button = ft.Container(
        width=150,
        height=150,
        border_radius=20,
        bgcolor=ft.colors.SURFACE_VARIANT,
        alignment=ft.alignment.center,
        on_click=load_save_page,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(name=ft.icons.SAVE_ROUNDED, size=48),
                ft.Text(value='Save Passwords', weight=ft.FontWeight.BOLD)
            ]
        )
    )

    check_button = ft.Container(
        width=150,
        height=150,
        border_radius=20,
        bgcolor=ft.colors.SURFACE_VARIANT,
        alignment=ft.alignment.center,
        on_click=load_test_page,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE_OUTLINED, size=48),
                ft.Text(value='Check Passwords', weight=ft.FontWeight.BOLD)
            ]
        )
    )

    home_page = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            gen_button,
            store_button,
            check_button
        ]
    )
    add_pass = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
        controls=[
            identifier_field_add,
            username_field_add,
            password_field,
            confirm_password_field,
            ft.FilledTonalButton(text="Done", width=150, on_click=add_new),
        ]
    )

    fetch_pass = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
        controls=[
            identifier_field_fetch,
            username_field_fetch,
            ft.Container(
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=ft.border_radius.all(25),
                width=50,
                height=50,
                tooltip='Get',
                content=ft.Icon(name=ft.icons.CONTENT_PASTE_SEARCH),
                on_click=fetch
            ),
        ]
    )

    delete_pass = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
        controls=[
            identifier_field_delete,
            username_field_delete,
            ft.Container(
                bgcolor=ft.colors.RED,
                border_radius=ft.border_radius.all(25),
                width=50,
                height=50,
                tooltip='Delete',
                content=ft.Icon(name=ft.icons.DELETE_OUTLINE_OUTLINED),
                on_click=delete_cred
            ),
        ]
    )

    gen_page = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    pass_length,
                    ft.Container(
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=ft.border_radius.all(25),
                        width=50,
                        height=50,
                        tooltip='Generate',
                        content=ft.Icon(name=ft.icons.MISCELLANEOUS_SERVICES_ROUNDED),
                        on_click=Generate

                    )
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        alignment=ft.alignment.center,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=ft.border_radius.all(5),
                        width=200,
                        height=50,
                        content=gen_pass
                    ),

                    ft.Container(
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=ft.border_radius.all(25),
                        width=50,
                        height=50,
                        tooltip='Copy',
                        content=ft.Icon(name=ft.icons.COPY),
                        on_click=Copy
                    )
                ]
            ),
        ]

    )

    save_page = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.FilledTonalButton(text="Add Password", width=150, on_click=add_clicked),
                    ft.FilledTonalButton(text="Fetch Password", width=155, on_click=fetch_clicked),
                    ft.FilledTonalButton(text="Delete Password", width=155, on_click=delete_clicked),
                ]
            ),
            fetch_pass,
            delete_pass,
            add_pass
        ]
    )

    test_page = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        auto_scroll=False,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    pass_test,
                    ft.Container(
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        border_radius=ft.border_radius.all(25),
                        width=50,
                        height=50,
                        tooltip='Test',
                        content=ft.Icon(name=ft.icons.RESTART_ALT_OUTLINED),
                        on_click=Test
                    )
                ]
            ),
            strong,
            medium,
            weak
        ]
    )

    main_page = ft.Container(
        height=page.window_height,
        width=page.window_width,
        expand=True,
        alignment=ft.alignment.center,
        content=home_page
    )

    page.appbar = ft.AppBar(
        center_title=True,
        leading=back_button,
        title=heading
    )
    page.snack_bar = ft.SnackBar(
        content=snack_bar_text,
        action="Done",
    )

    page.add(main_page)
    page.padding = 0
    page.theme_mode = 'light'
    page.window_max_width = 700
    page.window_max_height = 540
    page.window_min_height = 540
    page.window_min_width = 700
    page.window_maximizable = False
    page.update()


ft.app(target=main)
