"""
Forms for creating and deleting Register objects.

This module contains two Flask-WTF form classes used when working with
Register records:

- RegisterForm: Used when creating or editing a Register.
- RegisterDeleteForm: Used to confirm deletion of a Register.

Both forms use GOV.UK Frontend-styled WTForms widgets to match the
design system used in the application.
"""

from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovCheckboxInput,
    GovSubmitInput,
    GovTextInput,
)
from wtforms.fields import BooleanField, StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from app.models import Register


class RegisterForm(FlaskForm):
    """
    A form used to create or edit a Register.

    Fields
    ------
    name : StringField
        The human-readable name for the Register. This is required
        and must be unique across all Register records.
    submit : SubmitField
        A standard submit button.

    Custom Validation
    -----------------
    validate_name(field):
        WTForms automatically looks for methods named `validate_<fieldname>`
        and calls them when that field is validated.
        This method checks whether the chosen name already exists in the
        database and raises a ValidationError if so.
    """

    # A text field for entering the register name.
    # The `GovTextInput` widget makes it appear using GOV.UK styling.
    name = StringField(
        "Name",
        widget=GovTextInput(),
        validators=[InputRequired(message="Enter a name")],
    )

    # A standard GOV.UK-styled submit button.
    submit: SubmitField = SubmitField("Save", widget=GovSubmitInput())

    def __init__(self, register_id=None, **kwargs):
        super().__init__(**kwargs)
        self.register_id = register_id

    def validate_name(self, field):
        """
        Ensure that the register name is unique.

        Parameters
        ----------
        field : wtforms.fields.StringField
            The field object containing the value entered by the user.

        Raises
        ------
        ValidationError
            If a Register already exists with the same name.

        Notes
        -----
        - This method uses SQLAlchemy to query the database.
        - `first()` returns the first matching Register or None.
        - Raising a ValidationError tells WTForms that this field is invalid,
          and the error message is displayed to the user.
        - If there's no register ID, no special handling is applied when
          checking for errors.
        - If there is a register ID, it checks that the existing register
          matched by name has a different ID before throwing an error.
        """

        existing = Register.query.filter_by(name=field.data).first()

        if self.register_id == None:
            if existing:
                raise ValidationError("Name already in use")
        else:
            if existing and existing.id != self.register_id:
                raise ValidationError("Name already in use")


class RegisterDeleteForm(FlaskForm):
    """
    A form used to confirm the deletion of a Register.

    This form intentionally keeps the confirmation checkbox very explicit,
    to ensure users do not accidentally delete data.

    Fields
    ------
    confirm : BooleanField
        A checkbox that the user must tick to confirm deletion.
        If left unticked, the validation will fail and deletion will not occur.
    submit : SubmitField
        A GOV.UK-styled delete button.
    """

    # A checkbox that the user must actively tick to continue.
    # Using InputRequired ensures the user can't accidentally skip it.
    confirm = BooleanField(
        "I'm sure",
        widget=GovCheckboxInput(),
        validators=[InputRequired(message="Select if you want to delete this register")],
    )

    # Submit button styled using GOV.UK design system components.
    submit: SubmitField = SubmitField("Delete", widget=GovSubmitInput())
