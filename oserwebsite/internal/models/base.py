"""Base (abstract) models for internal."""

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class AddressMixin(models.Model):
    """Mixin that adds address-related fields to a Model.

    Fields
    ------
    line1 : char[100]
        First line of the address.
    line2 : char[100][blank]
        Second line of the address, not mendatory.
    post_code : char[20]
    city : char[50]
    country : FK[Country]

    Properties
    ----------
    address : str
        A multiline string displaying the full address:
            <line1>
            <line2>
            <postcode> <city>
            <country>
    address_inline : str
        A string displaying the full address, made to be used inline:
            <line1>, <line2>, <postcode> <city>, <country>
    """

    line1 = models.CharField(
        'adresse (ligne 1)', max_length=100,
        help_text="Numéro, rue, voie, nom de société, etc.")
    line2 = models.CharField(
        'adresse (ligne 2)', max_length=100, blank=True,
        help_text="Bâtiment, étage, lieu-dit, etc.")
    post_code = models.CharField(
        'code postal', max_length=20)
    city = models.CharField('ville', max_length=50)
    country = models.ForeignKey('Country',
                                models.SET_NULL, null=True,
                                verbose_name='pays')

    def _formatted_address(self, sep=', '):
        """Return a single-string formatted version of the address.

        The fields line1, line2, post_code, city and country are displayed
        in a sequence, separated by the specified sep string.

        Parameters
        ----------
        sep : str, optional
            Separator used to display the address.

        Example
        -------
        >>> a._formatted_address(sep=', ')
        3 rue Jean Maillard, Appt 140, 45600 Valence, France
        """
        city_line = '{} {}'.format(self.post_code, self.city.upper())
        _lines = (self.line1, self.line2, city_line,
                  self.country.name.upper())
        lines = [line for line in _lines if line]
        return mark_safe(sep.join(lines))

    @property
    def address_inline(self):
        return self._formatted_address(sep=', ')

    @property
    def address(self):
        return self._formatted_address(sep='<br/>')

    class Meta:  # noqa
        abstract = True


class Place(AddressMixin):
    """Represents a place that has an address."""

    name = models.CharField('nom', max_length=200)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'lieu'
        verbose_name_plural = 'lieux'
        ordering = ('name',)


class Profile(AddressMixin):
    """Abstract model representing a user profile.

    A user profile has a related django User, an address, a birthday and
    a phone.

    Fields
    ----------
    user : django.contrib.auth.models.User
    birthday : date[blank]
    phone : char[50][blank]

    Properties
    ----------
    first_name : str
        The django User's first name field.
    last_name : str
        The django User's last name field.
    full_name : str
        First name and last name, e.g. 'John Smith'.
    email : str
        The django User's email field.
    username : str
        The django User's username field.
    """

    user = models.OneToOneField(User, verbose_name='utilisateur')
    birthday = models.DateField('date de naissance',
                                null=True, blank=True)
    phone = models.CharField('téléphone',
                             max_length=50,
                             blank=True)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return self.user.get_full_name()
    full_name.fget.short_description = 'nom complet'

    def __str__(self):
        return self.full_name

    class Meta:  # noqa
        abstract = True


class Country(models.Model):
    """Represents a country."""

    name = models.CharField('nom', max_length=50)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = 'pays'
        verbose_name_plural = 'pays'
        ordering = ('name', )
