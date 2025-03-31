from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .v1.uploading import UploadView
import importlib


DEFAULT_API_VERSION = "v1"
####################
user_view = importlib.import_module(
    f"api.{DEFAULT_API_VERSION}.users.UsersView")
upload = importlib.import_module(
     f"api.{DEFAULT_API_VERSION}.uploading.UploadView"
)
##################
urlpatterns = [
     path('', views.index.as_view(), name="index"),
     path('<str:lang>/register/user/',
          user_view.CreateAuthUser.as_view(), name="register-user"),
       path('<str:lang>/checkUser/user/',
          user_view.CheckUser.as_view(), name="check-user"),
      path('<str:lang>/verifyemail/user/', 
           user_view.verifyAccount.as_view(), name="verify-email"),
            path('<str:lang>/passcode/user/', 
           user_view.setPassCode.as_view(), name="verify-email"),
     path('<str:lang>/register/api/user/',
          user_view.CreateApiUser.as_view(), name="register-api-user"),
     path('<str:lang>/make/deposit/',
          views.MakeDeposit.as_view(), name="make-deposit"),
     path('<str:lang>/make/card/deposit/',
          views.MakeDepositToBank.as_view(), name="make-card-deposit"),
     path('<str:lang>/get/deposit/',
          views.UserInvestmentSummary.as_view(), name="get-deposit"),
     path('<str:lang>/make/bank/withdraw/',
          views.MakeWithdrawFromBank.as_view(), name="make-bank-withdraw"),
     path('<str:lang>/make/goal/bank/withdraw/',
          views.MakeGoalWithdrawFromBank.as_view(),
          name="make-goal-bank-withdraw"),
     path('<str:lang>/make/mm/withdraw/',
          views.MakeWithdrawFromMobileMoney.as_view(),
          name="make-mm-withdraw"),
     path('<str:lang>/make/goal/mm/withdraw/',
          views.MakeGoalWithdrawFromMobileMoney.as_view(),
          name="make-goal-mm-withdraw"),
     path('<str:lang>/get/withdraw/',
          views.GetWithdrawsByAuthUser.as_view(), name="get-all-withdraws"),
     path('<str:lang>/get/investment/withdraws/',
          views.GetInvestmentWithdraws.as_view(),
          name="get-investment-withdraws"),
     path('<str:lang>/get/pending/withdraw/',
          views.GetPendingWithdrawsByAuthUser.as_view(),
          name="get-all-pending-withdraws"),
     path('<str:lang>/get/goal/withdraw/',
          views.GetWithdrawNetworths.as_view(), name="get-goal-withdraws"),
     path('<str:lang>/get/deposit/by/id/',
          views.GetDepositsById.as_view(), name="get-deposit-by-id"),
     path('<str:lang>/get/deposit/by/goal/<int:goalid>/',
          views.GetDepositsByGoalId.as_view(), name="get-deposit-by-goal"),
     path('<str:lang>/create/goal/',
          views.CreateGoal.as_view(), name="create-goal"),
     path('<str:lang>/create/goal/',
          views.Invite.as_view(), name="create-goal"),
      path('<str:lang>/invite/group/',
          views.CreateGroupGoal.as_view(), name="create-goal"),
     path('<str:lang>/edit/goal/',
          views.EditGoalz.as_view(), name="edit-goal"),
      path('<str:lang>/editgroupgoal/group/',
          views.EditGroupGoal.as_view(), name="edit-group-goal"),
      path('<str:lang>/delete/group/goal/',
          views.DeleteGroupGoal.as_view(), name="delete-goal"),
       path('<str:lang>/delete/group/pic/',
          views.DeleteGroupPic.as_view(), name="delete-pic"),
       path('<str:lang>/change/group/pic/',
          views.ChangeGroupPic.as_view(), name="change- group-pic"),
     path('<str:lang>/delete/goal/',
          views.DeleteGoalz.as_view(), name="delete-goal"),
     path('<str:lang>/newgroup/group/',
          views.NewGroup.as_view(), name="new-group"),
     path('<str:lang>/getgroup/group/',
          views.GetGroup.as_view(), name="new-group"),
     path('<str:lang>/editgroup/group/',
          views.EditGroup.as_view(), name="edit-group"),
     path('<str:lang>/addmembers/group/',
          views.AddMembers.as_view(), name="add-members"),
     path('<str:lang>/details/group/',
          views.DetailsGroup.as_view(), name="new-group"),
     path('<str:lang>/get/user/verification/',
          user_view.IsUserVerified.as_view(), name="get-user-verification"),
     path('<str:lang>/get/verification/',
          views.IsVerified.as_view(), name="get-verification"),
     path('<str:lang>/resend/verification/email/',
          user_view.ResendVerificationEmail.as_view(),
          name="resend-verification-email"),
     path('<str:lang>/simple/email/',
          user_view.SendSimpleEmail.as_view(),
          name="sample-email"),
     path('<str:lang>/invest/email/',
          user_view.SimpleEmail.as_view(),
          name="invest-email"),
     path('<str:lang>/get/risk/analysis/percentages/',
          views.GetRiskAnalysisPercentages.as_view(),
          name="get-risk-analysis-percentages"),
     path('<str:lang>/user/nextOfKin/',
          views.AddNextOfKin.as_view(), name="add-nextOfKin"),
     path('<str:lang>/get/nextOfKin/',
          views.GetNextOfKin.as_view(), name="get-nextOfKin"),
     path('<str:lang>/get/user/goal/',
          views.GetGoalsByAuthUser.as_view(), name="get-user-goal"),
     path('<str:lang>/get/goal/by/id/',
          views.GetGoalById.as_view(), name="get-goal-by-id"),
     path('<str:lang>/get/withdraw/fee/',
          views.GetWithdrawFee.as_view(), name="get-withdraw-fee"),
     path('<str:lang>/make/goal/deposit/',
          views.MakeDepositToGoal.as_view(), name="deposit-to-goal"),
     path('<str:lang>/make/subscription/',
          views.Subscribe.as_view(), name="make-subscription"),
     path('<str:lang>/get/subscription/status/',
          views.GetSubscriptionStatus.as_view(),
          name="get-subscription-status"),
     path('<str:lang>/auth/user/login/',
          user_view.LoginUserAuthToken.as_view(), name="login-user"),
     path('<str:lang>/auth/user/passcode/',
          user_view.LoginWithPasscode.as_view(), name="login-user"),
     path('<str:lang>/auth/token/',
          views.CreateUserAuthToken.as_view(), name="create-user-token"),
     path('<str:lang>/auth/user/',
          user_view.GetAuthUser.as_view(), name="get-auth-user"),
     path('<str:lang>/auth/user/email/',
          user_view.GetAuthUserByEmail.as_view(),
          name="get-auth-user-by-email"),
     path('<str:lang>/auth/user/riskprofile/',
          views.AddRiskProfile.as_view(), name="add-risk-profile"),
     path('<str:lang>/auth/get/riskprofile/',
          views.GetRiskProfile.as_view(), name="get-risk-profile"),
     path('<str:lang>/auth/user/<int:userid>/',
          user_view.GetAuthUserById.as_view(), name="get-auth-user-by-id"),
     path('<str:lang>/auth/users/all/',
          user_view.GetAllUsers.as_view(), name="get-all-users"),
     path('<str:lang>/auth/fundmanagers/all/',
          user_view.GetAllFundManagers.as_view(),
          name="get-all-fund-managers"),
     path('<str:lang>/auth/user/banks/',
          views.GetCountryBanks.as_view(), name="get-all-banks-by-country"),
     path('<str:lang>/auth/users/emails/all/',
          user_view.GetAllUsersEmails.as_view(), name="get-all-users-emails"),
     path('<str:lang>/auth/user/networth/',
          views.GetGoalNetworth.as_view(), name="get-user-networth"),
     path('<str:lang>/auth/get/investment/options/',
          views.GetInvestmentOption.as_view(), name="get-investment-options"),
     path('<str:lang>/auth/get/investment/classes/',
          views.GetInvestmentClasses.as_view(), name="get-investment-classes"),
     path('<str:lang>/auth/user/networth/data/',
          views.GetUserActualNetworthData.as_view(),
          name="get-user-networth-data"),
     path('<str:lang>/auth/get/investment/option/',
          views.GetInvestmentOptionByName.as_view(),
          name="get-investment-option-by-name"),
     path('<str:lang>/auth/get/investment/class/options/',
          views.GetInvestmentOptionsByClass.as_view(),
          name="get-investment-options-by-class"),
     path('<str:lang>/auth/get/fund/investment/class/',
          views.GetInvestmentOptionsByFund.as_view(),
          name="get-investment-options-by-fund"),
     path('<str:lang>/auth/get/investment/option/units/',
          views.GetInvestmentOptionById.as_view(),
          name="get-investment-option-units"),
     path('<str:lang>/auth/user/upload/profile/photo/',
          UploadView.UploadPhoto.as_view(), name="upload-photo"),
     path('<str:lang>/auth/upload/goal/photo/',
          UploadView.UploadGoalPhoto.as_view(), name="upload-goal-photo"),
     path('<str:lang>/auth/user/account/type/',
          views.AddAccountTypes.as_view(), name="add-account-types"),
     path('<str:lang>/auth/user/update/password/',
          user_view.ChangeForgotPassword.as_view(),
          name="update-user-password"),
     path('<str:lang>/password/reset/',
          user_view.InitPasswordReset.as_view(), name="password-reset"),
     path('<str:lang>/email/verify/<str:userid>/',
          user_view.verifyAccount.as_view(),
          name="email-verify"),
     path('<str:lang>/onboard/', user_view.OnboardAuthUsers.as_view(),
          name="onboard-users"),
     path('<str:lang>/onboard/ortus/users/',
          user_view.OnboardOrtusUsers.as_view(),
          name="onboard-ortus-users"),
     path('<str:lang>/onboard/ortus/users/track/',
          views.OnboardOrtusUsersTrack.as_view(),
          name="onboard-ortus-users-track"),
     path('<str:lang>/auth/user/delete/',
          user_view.DeleteUserAccount.as_view(),
          name="delete-user-account"),
     path('deposit/', views.DepositDataSet.as_view(),
          name="deposit-data-set"),
     path('<str:lang>/users/deposits/',
          views.OnboardAuthUsersDeposits.as_view(),
          name="all-user-deposits"),
     path('<str:lang>/users/withdraws/',
          views.OnboardAuthUsersWithdraws.as_view(),
          name="all-user-withdraws"),
     path('<str:lang>/onboard/investment/tracks/',
          views.OnboardInvestmentTrack.as_view(),
          # as_view() - can cause crsf error
          name="onboard-investemnt-tracks"),
     path('<str:lang>/get/user/track/',
          views.GetUserInvestmentTrack.as_view(),
          # as_view() - can cause crsf error
          name="get-user-track"),
     path('<str:lang>/requestpaymentshook/',
          views.RequestPaymentHook.as_view(),
          name="request-payment-hook"),
     path('<str:lang>/validate/mm/number/',
          views.ValidateMMNumber.as_view(),
          name="validate-mm-number"),
     path('<str:lang>/request/payment/',
          views.RequestPayment.as_view(),
          name="request-payment"),
     path('<str:lang>/get/transaction/',
          views.GetTransactionByReference.as_view(),
          name="get-transaction-by-reference"),
]
urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
