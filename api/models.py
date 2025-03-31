from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

class SupportedLanguage(models.Model):
    lang_name = models.CharField(max_length=255)
    lang_iso_code = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.lang_name


#######################################


class SupportedCountry(models.Model):
    coutry_name = models.CharField(max_length=255)
    coutry_flag = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.coutry_name


class TimeZone(models.Model):
    country = models.ForeignKey(
        SupportedCountry, on_delete=models.CASCADE, null=True, blank=True
    )
    dispaly_name = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    has_been_modified = models.BooleanField(default=False)
    last_modified = models.DateTimeField()

    def __str__(self):
        return "%s" % self.dispaly_name


class UserType(models.Model):
    type_name = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.type_name


# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=200, default="personal", null=True)
    country = models.CharField(max_length=200, default="uganda", null=True)
    language = models.ForeignKey(
        SupportedLanguage, on_delete=models.CASCADE, null=True, blank=True
    )
    tmz = models.ForeignKey(TimeZone, on_delete=models.CASCADE, null=True, blank=True)
    company_category = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    phoneno = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    verification_code = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    coi = models.FileField(null=True, blank=True)
    moa = models.FileField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile", default="default_picture.jpg"
    )
    logo = models.ImageField(
        upload_to="api_profile", default="default_logo.jpg"
    )
    bankname = models.CharField(max_length=255, null=True, blank=True)
    banknumber = models.CharField(max_length=255, null=True, blank=True)
    bankbranch = models.CharField(max_length=255, null=True, blank=True)
    bankaccname = models.CharField(max_length=255, null=True, blank=True)
    passcode = models.CharField(max_length=255, null=True, blank=True)
    phone_hash = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    company_profile = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class NextOfKin(models.Model):
    first_name = models.CharField(
        verbose_name="first name", default="first name", max_length=200
    )
    last_name = models.CharField(
        verbose_name="last name", default="last name", max_length=200
    )
    phone = models.IntegerField(verbose_name="phone", default="+256 000 000 000")
    email = models.EmailField(verbose_name="email", default="nextofkin@gmail.com")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.first_name


class RiskAnalysis(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    cash = models.FloatField(default=0)
    credit = models.FloatField(default=0)
    venture = models.FloatField(default=0)
    absolute_return = models.FloatField(default=0)
    score_min = models.IntegerField(default=0)
    score_max = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s" % self.name


class RiskProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qn1 = models.CharField(max_length=200, default="saving", verbose_name="objectives")
    qn2 = models.CharField(
        max_length=200, default="less_than_year", verbose_name="horizon"
    )
    qn3 = models.CharField(
        max_length=200, default="treasuries", verbose_name="past investing"
    )
    qn4 = models.CharField(
        max_length=200, default="less_ten_percent", verbose_name="portfolio max loss"
    )
    qn5 = models.CharField(max_length=200, default="least", verbose_name="capital")
    qn6 = models.CharField(
        max_length=200, default="employment", verbose_name="funds source"
    )
    qn7 = models.CharField(
        max_length=200, default="guaranteed_returns", verbose_name="goals"
    )
    qn8 = models.CharField(max_length=200, default="A", verbose_name="profit or loss")
    qn9 = models.CharField(max_length=200, default="no", verbose_name="risk")
    qn10 = models.CharField(
        max_length=200, default="no", verbose_name="future investing"
    )
    qn11 = models.CharField(
        max_length=200, default="comfortable", verbose_name="inflation impact"
    )
    created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(verbose_name="score", default=0)
    risk_analysis = models.ForeignKey(RiskAnalysis, on_delete=models.CASCADE, null=True, blank=True)
    investment_option = models.CharField(
        max_length=200,
        verbose_name="investment option",
        default="Automatic Asset Allocation",
    )
    is_complete = models.BooleanField(default=False, verbose_name="status")

    def __str__(self):
        return "%s" % self.user.first_name


class MerchantApp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s | %s| %s" % (str(self.user), self.app_name, self.api_key)


class Currency(models.Model):
    country = models.ForeignKey(
        SupportedCountry, on_delete=models.CASCADE, null=True, blank=True
    )
    currency_locale = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=255)
    currency_symbol = models.CharField(max_length=255)
    exchange_rate = models.FloatField(max_length=500)
    is_indented = models.BooleanField(default=False)
    is_infront = models.BooleanField(default=True)
    decimal_points = models.IntegerField(default=2)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.currency_locale


# Main Application Modules


class Module(models.Model):
    module_name = models.CharField(max_length=255)
    code_name = models.CharField(max_length=255)
    route_name = models.CharField(max_length=255)
    is_a_sub_module = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    main_module_id = models.IntegerField(null=True, blank=True)
    sort_value = models.IntegerField()
    depth = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.module_name


# Side Menu Modules


class SideMenu(models.Model):
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING)
    sort_value = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.module


# Dashboard menu model


class DashboardMenu(models.Model):
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING)
    sort_value = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.module.module_name


class NavigationMenu(models.Model):
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING)
    sort_value = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.module.module_name


class PaymentType(models.Model):
    payment_name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=200)
    payment_logo = models.CharField(max_length=200, null=True, blank=True)
    sort_value = models.IntegerField(default=0)
    has_standarded_charge = models.BooleanField(default=False)
    payment_charge = models.FloatField(default=0, blank=True, null=True)
    charge_in_percentage = models.BooleanField(default=True)
    charge_fees_on_user = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.payment_name


class PaymentMethod(models.Model):
    en_payment_method_name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.en_payment_method_name


class PaymentOption(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING)
    en_payment_option_name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=200)
    payment_option_logo = models.CharField(max_length=200, null=True, blank=True)
    sort_value = models.IntegerField(default=0)
    has_standarded_charge = models.BooleanField(default=False)
    payment_charge = models.FloatField(default=0, blank=True, null=True)
    charge_in_percentage = models.BooleanField(default=True)
    charge_fees_on_user = models.BooleanField(default=True)
    has_pre_inputs = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s [%s]" % (self.en_payment_option_name, self.code_name)


class PaymentOptionField(models.Model):
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.DO_NOTHING)
    en_entry_name = models.CharField(max_length=500)
    entry_code_name = models.CharField(max_length=255)
    has_entry_value = models.BooleanField(default=False)
    entry_value = models.CharField(max_length=500, null=True, blank=True)
    is_a_float = models.BooleanField(default=False)
    is_a_int = models.BooleanField(default=False)
    is_a_string = models.BooleanField(default=True)
    is_required = models.BooleanField(default=True)
    is_default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[%s] %s : %s" % (
            str(self.payment_option),
            self.en_entry_name,
            str(self.entry_value),
        )


class PaymentOptionSetting(models.Model):
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.DO_NOTHING)
    en_entry_name = models.CharField(max_length=500)
    entry_code_name = models.CharField(max_length=255)
    has_entry_value = models.BooleanField(default=False)
    entry_value = models.CharField(max_length=500, null=True, blank=True)
    is_required = models.BooleanField(default=True)
    is_default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[%s] %s : %s" % (
            str(self.payment_option),
            self.en_entry_name,
            str(self.entry_value),
        )


class PaymentOptionSupport(models.Model):
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(SupportedCountry, on_delete=models.DO_NOTHING)
    is_disabled = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s (%s)" % (self.payment_option, self.country)


class PaymentTypeOption(models.Model):
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.DO_NOTHING)
    is_disabled = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s (%s)" % (self.payment_option, self.payment_option)


class RegionalPaymentType(models.Model):
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(SupportedCountry, on_delete=models.DO_NOTHING)
    sort_value = models.IntegerField()
    is_disabled = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    has_been_modified = models.BooleanField(default=False)
    last_modified = models.DateTimeField()

    def __str__(self):
        return "%s (%s)" % (self.payment_type, self.country)


class PaymentTypeSetting(models.Model):
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    entry_name = models.CharField(max_length=500)
    entry_code_name = models.CharField(max_length=255)
    has_entry_value = models.BooleanField(default=False)
    entry_value = models.CharField(max_length=500, null=True, blank=True)
    is_required = models.BooleanField(default=True)
    is_default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[%s] %s : %s" % (
            str(self.payment_type),
            self.entry_name,
            str(self.entry_value),
        )


class AccountType(models.Model):
    type_name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    sort_value = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.type_name


class BankTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=200)
    bank_code = models.CharField(max_length=200)
    reference_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=200)
    created = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % self.reference_id


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=200, null=True)
    goal_period = models.IntegerField(default="1", null=True)
    goal_amount = models.BigIntegerField(default=0)
    deposit_type = models.CharField(max_length=200, null=True)
    deposit_reminder_day = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=False)
    goal_picture = models.ImageField(
        upload_to="goal", default="default_picture.jpg"
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s - %s" % (self.user, self.goal, self.goal_amount)


# class FundManager(models.Model):
#     type = models.CharField(max_length=200, default="fundmanager", null=True)
#     country = models.CharField(max_length=200, blank=True, null=True)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     bio = models.CharField(max_length=255, null=True, blank=True)
#     company_profile = models.CharField(max_length=255, null=True, blank=True)
#     phoneno = models.CharField(max_length=255, null=True, blank=True)
#     email = models.EmailField(max_length=30, null=True, blank=True)
#     password = models.CharField(max_length=255, null=True, blank=True)
#     is_verified = models.BooleanField(default=0)
#     bankname = models.CharField(max_length=255, null=True, blank=True)
#     banknumber = models.CharField(max_length=255, null=True, blank=True)
#     bankbranch = models.CharField(max_length=255, null=True, blank=True)
#     bankaccname = models.CharField(max_length=255, null=True, blank=True)
#     profile_picture = models.ImageField(
#         upload_to="profile", default="default_picture.jpg"
#     )
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "%s" % self.name


class InvestmentClass(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(
        upload_to="investmentClasses", default="default_picture.jpg"
    )

    def __str__(self):
        return "%s" % self.name


class InvestmentOption(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    class_type = models.ForeignKey(InvestmentClass, on_delete=models.CASCADE, null=True, blank=True)
    fund_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    minimum = models.BigIntegerField(default=0)
    interest = models.IntegerField(default=0)
    status = models.BooleanField(default=0)
    units = models.FloatField(default=0)
    description = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.name


class InvestmentPerformance(models.Model):
    investment_option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE, null=True, blank=True)
    fund_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    bought = models.BigIntegerField(default=0)
    selling = models.BigIntegerField(default=0)
    performance_fee = models.IntegerField(default=0)
    units = models.FloatField(default=0)
    status = models.BooleanField(default=False)
    management_fee = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.fund_manager, self.investment_option)


class FundWithdraw(models.Model):
    fund_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    withdarw_amount = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %d" % self.fund_manager % self.withdarw_amount


class Fund(models.Model):
    fund_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    deposit_amount = models.BigIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %d" % self.fund_manager % self.withdarw_amount


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE, null=True, blank=True)
    payment_means = models.CharField(max_length=200, null=True)
    deposit_category = models.CharField(max_length=200, null=True)
    deposit_amount = models.FloatField(default=0)
    currency = models.CharField(max_length=200, default="UGX")
    account_type = models.ForeignKey(AccountType, on_delete=models.DO_NOTHING)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=200, default="")
    reference_id = models.IntegerField(default=0, null=True)
    txRef = models.CharField(max_length=200, null=True)
    available = models.BooleanField(default=0)
    updated = models.DateTimeField(null=True, blank=True)
    units = models.FloatField(default=0)

    def __str__(self):
        return "%s - %s" % (self.user, self.deposit_amount)


# temporarily change auto timedate
class InvestmentTrack(models.Model):
    # goals are also part of the risk profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE, null=True, blank=True)
    withdraw_amount = models.FloatField(default=0)
    deposit_amount = models.FloatField(default=0)
    opening_balance = models.FloatField(default=0)
    interest = models.FloatField(default=0)
    management_fee = models.FloatField(default=0)
    performance_fee = models.FloatField(default=0)
    closing_balance = models.FloatField(default=0)
    risk_profile = models.BooleanField(default=False)
    out_performance = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.closing_balance)
    

class Transaction(models.Model):
    # goals are also part of the risk profile
    status = models.CharField(max_length=200, null=True)
    message = models.CharField(max_length=200, null=True)
    customer_reference = models.CharField(max_length=200, null=True)
    internal_reference = models.CharField(max_length=200, null=True)
    msisdn = models.CharField(max_length=200, null=True)
    amount = models.FloatField(default=0)
    currency = models.CharField(max_length=200, null=True)
    provider = models.CharField(max_length=200, null=True)
    charge = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s" % (self.msisdn, self.amount)


# class Withdraw(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     withdraw_channel = models.CharField(max_length=200, default="bank")
#     withdraw_amount = models.FloatField(default=0)
#     currency = models.CharField(max_length=200, default="UGX")
#     account_type = models.ForeignKey(AccountType, on_delete=models.DO_NOTHING)
#     created = models.DateTimeField(auto_now_add=True)
#     goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
#     investment_option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE, null=True, blank=True)
#     transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE, null=True, blank=True)
#     status = models.CharField(max_length=200, default="")
#     units = models.FloatField(default=0)

#     def __str__(self):
#         return "%s - %s" % (self.user, self.withdraw_amount)

# edited without transfer initiation
class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    withdraw_channel = models.CharField(max_length=200, default="bank")
    withdraw_amount = models.FloatField(default=0)
    currency = models.CharField(max_length=200, default="UGX")
    account_type = models.ForeignKey(AccountType, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
    investment_option = models.ForeignKey(InvestmentOption, on_delete=models.CASCADE, null=True, blank=True)
    transaction = models.ForeignKey(BankTransaction, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=200, default="")
    units = models.FloatField(default=0)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    account_bank = models.CharField(max_length=255, null=True, blank=True)
    charge_amount = models.FloatField(default=0)

    def __str__(self):
        return "%s - %s" % (self.user, self.withdraw_amount)


class DepositType(models.Model):
    type_name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.type_name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)
    days_left = models.IntegerField(default=30)
    reference_id = models.IntegerField(default=0)
    reference = models.CharField(max_length=200)
    amount = models.BigIntegerField(default=0)
    currency = models.CharField(max_length=200, default="UGX")
    created = models.DateTimeField(auto_now_add=True)
    txRef = models.CharField(max_length=200)
    was_displayed = models.BooleanField(default=0)

    def __str__(self):
        return "%s" % self.is_subscribed


class HealthCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_subscribed_overall = models.BooleanField(default=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    was_displayed = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.is_subscribed_overall


class Networth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.amount


class DepositTime(models.Model):
    time_name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=200)
    is_default = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.time_name


class Account(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=500)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)  # Default currency
    opening_balance = models.FloatField(default=0)
    account_no = models.CharField(max_length=300)
    is_operational_account = models.BooleanField(default=False)
    is_cash_account = models.BooleanField(default=False)
    is_reconcilable = models.BooleanField(default=False)
    allow_over_drafts = models.BooleanField(default=False)
    narration = models.CharField(max_length=3000, null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    is_editable = models.BooleanField(default=True)
    is_deletable = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.account_name


# Ledger Entries or Account Entries or Account Ledgers
class LedgerEntry(models.Model):
    ledger_no = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=255)
    is_adjusting_entry = models.BooleanField(default=False)
    amount = models.FloatField(default=0)
    narration = models.CharField(max_length=5000, null=True, blank=True)
    is_disabled = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.account, self.amount)


class TopUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topup_amount = models.BigIntegerField(default=0)
    account_type = models.ForeignKey(AccountType, on_delete=models.DO_NOTHING)
    transactioncode = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.topup_amount
    
    


# Group model for group texting
class Group(models.Model):
    name = models.CharField(max_length=255)  # Group name
    description = models.TextField(blank=True, null=True)  # Optional group description
    profile_pic = models.ImageField(upload_to='group_pics/', blank=True, null=True)  # Group profile picture
    created_at = models.DateTimeField(auto_now_add=True)  # Group creation time
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')  # Group creator
    last_activity = models.DateTimeField(auto_now=True)  # Last activity timestamp

    def __str__(self):
        return self.name

class GroupDeposit(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='deposits')  # Link to the Group model
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_deposits')  # Link to the User model
    deposit_amount = models.DecimalField(max_digits=15, decimal_places=2)  # Amount deposited
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)  # Link to Currency model, default to ID 1 (e.g., UGX)
    deposit_date = models.DateTimeField()  # Date and time of the deposit
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])  # Status of the deposit
    reference = models.CharField(max_length=100, unique=True, blank=True, null=True)  # Unique transaction reference
    created_at = models.DateTimeField(auto_now_add=True)  # When the deposit record was created
    updated_at = models.DateTimeField(auto_now=True)  # When the deposit record was last updated

    def __str__(self):
        return f"{self.member.username} - {self.group.name} - {self.deposit_amount} {self.currency.currency_code}"

# New GroupGoal model
class GroupGoal(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='goals')
    goal_name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active', choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.group.name} - {self.goal_name} - {self.target_amount}"
    class Meta:
        verbose_name = "Group Goal"
        verbose_name_plural = "Group Goals"
        ordering = ['-start_date']

# Participant model to track group members
class Participant(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='participants')  # Group the participant belongs to
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_participations')  # User in the group
    role = models.CharField(max_length=50, default='member')  # Role in the group (e.g., admin, member)
    joined_at = models.DateTimeField(auto_now_add=True)  # When the user joined the group
    muted = models.BooleanField(default=False)  # Whether the user has muted the group

    class Meta:
        unique_together = ('group', 'user')  # Ensure a user can only join a group once

    def __str__(self):
        return f'{self.user.username} in {self.group.name}'

class GroupGoalDeposit(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='goal_deposits')
    goal = models.ForeignKey(GroupGoal, on_delete=models.CASCADE, related_name='deposits')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_goal_deposits')
    deposit_amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, default=1)
    deposit_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    reference = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member.username} - {self.goal.goal_name} - {self.deposit_amount} {self.currency.currency_code}"

    class Meta:
        verbose_name = "Group Goal Deposit"
        verbose_name_plural = "Group Goal Deposits"
        ordering = ['-deposit_date']
# Media model for handling attachments (images, audio, etc.)

class GroupInvitation(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='invitations')
    token = models.CharField(max_length=64, unique=True, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_invites')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # When the link stops working
    max_uses = models.PositiveIntegerField(default=1)  # 0 = unlimited uses
    uses = models.PositiveIntegerField(default=0)  # How many times it's been used
    is_active = models.BooleanField(default=True)  # Can be manually disabled

    class Meta:
        verbose_name = "Group Invitation"
        verbose_name_plural = "Group Invitations"
        indexes = [
            models.Index(fields=['token']),  # Faster lookups for token-based access
        ]

    def __str__(self):
        return f"Invite for {self.group.name} (Expires: {self.expires_at})"

    def save(self, *args, **kwargs):
        if not self.token:  # Auto-generate token if new
            self.token = secrets.token_urlsafe(32)  # Cryptographically secure
        if not self.expires_at:  # Default expiry: 7 days
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        super().save(*args, **kwargs)

    def is_valid(self):
        """Check if the invite can still be used."""
        return (
            self.is_active and
            (self.max_uses == 0 or self.uses < self.max_uses) and
            timezone.now() < self.expires_at
        )

    def mark_used(self):
        """Increment usage count and deactivate if max uses reached."""
        self.uses += 1
        if self.max_uses > 0 and self.uses >= self.max_uses:
            self.is_active = False
        self.save()
class Media(models.Model):
    file_path = models.FileField(upload_to='media/')  # Path to the media file
    type = models.CharField(max_length=50)  # Type of media (e.g., image, audio, video)
    mime_type = models.CharField(max_length=100, blank=True, null=True)  # MIME type of the file
    file_size = models.IntegerField(blank=True, null=True)  # Size of the file in bytes
    duration = models.IntegerField(blank=True, null=True)  # Duration for audio/video files
    thumbnail_path = models.FileField(upload_to='thumbnails/', blank=True, null=True)  # Thumbnail for media
    created_at = models.DateTimeField(auto_now_add=True)  # When the media was uploaded
    deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return f'{self.type} - {self.file_path}'


# Message model for group texting
class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')  # Group the message belongs to
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # User who sent the message
    message = models.TextField(blank=True, null=True)  # Text content of the message
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, null=True)  # Attached media (if any)
    type = models.CharField(max_length=50, default='text')  # Type of message (e.g., text, image, audio)
    status = models.CharField(max_length=50, default='sent')  # Status of the message (e.g., sent, delivered, read)
    timestamp = models.DateTimeField(auto_now_add=True)  # When the message was sent
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='replies')  # Reply to another message
    reply_to_message = models.TextField(blank=True, null=True)  # Text of the replied message
    forwarded = models.BooleanField(default=False)  # Whether the message was forwarded
    edited = models.BooleanField(default=False)  # Whether the message was edited
    deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return f'{self.sender.username}: {self.message}'    
