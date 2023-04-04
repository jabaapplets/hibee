from hibeeforms import CharField, Form, Textarea
from hibeeutils.safestring import mark_safe

from .base import WidgetTest


class TextareaTest(WidgetTest):
    widget = Textarea()

    def test_render(self):
        self.check_html(
            self.widget,
            "msg",
            "value",
            html=('<textarea rows="10" cols="40" name="msg">value</textarea>'),
        )

    def test_render_required(self):
        widget = Textarea()
        widget.is_required = True
        self.check_html(
            widget,
            "msg",
            "value",
            html='<textarea rows="10" cols="40" name="msg">value</textarea>',
        )

    def test_render_empty(self):
        self.check_html(
            self.widget,
            "msg",
            "",
            html='<textarea rows="10" cols="40" name="msg"></textarea>',
        )

    def test_render_none(self):
        self.check_html(
            self.widget,
            "msg",
            None,
            html='<textarea rows="10" cols="40" name="msg"></textarea>',
        )

    def test_escaping(self):
        self.check_html(
            self.widget,
            "msg",
            'some "quoted" & ampersanded value',
            html=(
                '<textarea rows="10" cols="40" name="msg">'
                "some &quot;quoted&quot; &amp; ampersanded value</textarea>"
            ),
        )

    def test_mark_safe(self):
        self.check_html(
            self.widget,
            "msg",
            mark_safe("pre &quot;quoted&quot; value"),
            html=(
                '<textarea rows="10" cols="40" name="msg">pre &quot;quoted&quot; value'
                "</textarea>"
            ),
        )

    def test_fieldset(self):
        class TestForm(Form):
            template_name = "forms_tests/use_fieldset.html"
            field = CharField(widget=self.widget)

        form = TestForm()
        self.assertIs(self.widget.use_fieldset, False)
        self.assertHTMLEqual(
            '<div><label for="id_field">Field:</label>'
            '<textarea cols="40" id="id_field" name="field" '
            'required rows="10"></textarea></div>',
            form.render(),
        )
