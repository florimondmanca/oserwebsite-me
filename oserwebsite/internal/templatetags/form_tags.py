"""Form-related template tags."""
from django import template

register = template.Library()


@register.inclusion_tag('forms/field.html')
def form_field(field, addon="", icon=""):
    """Render a form field.

    Parameters
    ----------
    field : forms.FormField
        The field to render.
    addon : str, optional
        If passed, the field will be a form-group and the addon string
        will be rendered beside the field.
    icon : str, optional
        Same as addon but renders an AwesomeFont icon instead of bare string.

    """
    return {'field': field, 'icon': icon, 'addon': addon}


@register.inclusion_tag('forms/column_form.html')
def column_form(form, title="", description="", id="form",
                submit_label="Submit"):
    """Render a form as a column.

    Parameters
    ----------
    form : forms.Form
        Django Form to render.
    title : str, optional
        Title that will be displayed at the top of the form. None by default.
    description : str, optional
        Form description that will be displayed below the title. None by
        default.
    id : str, optional
        The <form> HTML tag will be given this id. Default is #form.
    submit_label : str, optional
        The text displayed on the submit button.
    """
    return {'form': form, 'title': title, 'description': description,
            'id': id, 'submit_label': submit_label}
