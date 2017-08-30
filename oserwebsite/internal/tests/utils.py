"""Generic test function generators and other test utilities."""


class GenericModelTests:
    """Class for creating generic tests for a model."""

    def __init__(self, model_cls, sampler):
        self.model_cls = model_cls
        self.sampler = sampler

    def sample(self):
        return self.sampler(self.model_cls)

    def field_verbose_name(self, field_name, verbose_name):
        """Test that model field has given verbose name."""
        def test_verbose_name(this):
            obj = self.sample()
            label = obj._meta.get_field(field_name).verbose_name
            this.assertEqual(verbose_name, label)

        return test_verbose_name

    def field_max_length(self, field_name, max_length):
        """Test that model field has given max_length."""
        def test_max_length(this):
            obj = self.sample()
            length = obj._meta.get_field(field_name).max_length
            this.assertEqual(max_length, length)

        return test_max_length

    def verbose_name(self, verbose_name):
        """Test that model has given verbose name."""
        def test_model_verbose_name(this):
            label = self.model_cls._meta.verbose_name
            this.assertEqual(verbose_name, label)

        return test_model_verbose_name

    def property_verbose_name(self, property_name, verbose_name):
        """Test that model property has given verbose name."""
        def test_verbose_name(this):
            p = getattr(self.model_cls, property_name)
            label = p.fget.short_description
            this.assertEqual(verbose_name, label)

        return test_verbose_name

    def property_value(self, property_name, property_value):
        """Test that sampled model instance property is given value."""
        def test_property_value(this):
            obj = self.sample()
            value = getattr(obj, property_name)
            this.assertEqual(property_value, value)

        return test_property_value

    def absolute_url(self, url):
        """Test that sampled model instance's absolute_url is given url."""
        def test_absolute_url(this):
            obj = self.sample()
            this.assertEqual(url, obj.get_absolute_url())

        return test_absolute_url

    def str(self, s):
        """Test that sampled model instance __str__ is given string."""
        def test_str(this):
            obj = self.sample()
            this.assertEqual(s, str(obj))

        return test_str
