from application.base import BaseManager, render_jinja
from flask import Blueprint, request
render = render_jinja('static/templates/modal', encoding='utf-8',)

class ConfirmModal(BaseManager):
    def get(self):
        return render.modal()
app = Blueprint('modal_app', __name__, template_folder='templates')
app.add_url_rule('', view_func=ConfirmModal.as_view('modal'))