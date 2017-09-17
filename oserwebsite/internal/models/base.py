"""Base (abstract) models for internal."""

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class AddressMixin(models.Model):
    """Mixin that adds address-related fieldsto a Model.

    Properties
    ----------
    address : str
        A multiline string displaying the full address.
    address_inline : str
        A string displaying the full address, made to be used inline.
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

    def _address_separated(self, sep=', '):
        city_line = '{} {}'.format(self.post_code, self.city.upper())
        _lines = (self.line1, self.line2, city_line,
                  self.country.name.upper())
        lines = list(filter(None, _lines))
        return mark_safe(sep.join(lines))

    @property
    def address_inline(self):
        return self._address_separated(sep=', ')

    @property
    def address(self):
        return self._address_separated(sep='<br/>')

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

    Attributes
    ----------
    user : django.contrib.auth.models.User
    birthday : date
    phone : str

    Properties
    ----------
    first_name : str
    last_name : str
    full_name : str
    email : str
    username : str
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


class NameModel(models.Model):
    """Model that only has a name field.

    The model's string representation is its name.
    """

    name = models.CharField('nom', max_length=30)

    def __str__(self):
        return self.name

    class Meta:  # noqa
        abstract = True


class Country(NameModel):
    """Represents a country."""

    class Meta:  # noqa
        verbose_name = 'pays'
        verbose_name_plural = 'pays'
        ordering = ('name', )
