"""http://developer.authorize.net/api/reference/#customer-profiles-get-customer-payment-profile-list"""
import os
import sys
import time
import importlib
import util
import argparse

from pprint import pprint
#import constants

from datetime import datetime, timedelta
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
#constants = importlib.import_module('constants.py')

AUTH_NET_ENVIRONMENT = "https://api2.authorize.net/xml/v1/request.api"
TRANSACTION_KEY = "2n73S669smL8UXEe"
API_ID = "2FGhZ4s5P"


outDict = dict()


def get_customer_payment_profile_list():
    """Retrieve a list of customer payment profiles matching the specific search parameters"""

    # Create a merchantAuthenticationType object with authentication details
    # retrieved from the constants file
    merchant_auth = apicontractsv1.merchantAuthenticationType()
    merchant_auth.name = API_ID
    merchant_auth.transactionKey = TRANSACTION_KEY
    #merchant_auth.clientKey.transactionKey = "9QTSZu9Zt8TYsSe63vj46k6tM8tn8cdb2jz4QgBPQKd8UPWNsXZaESgP55jaX2pm"

    #merchant_auth.transactionKey = "2a14f5122e29fdd00771"
    # Set the transaction's refId
    ref_id = "ref{}".format(int(time.time())*1000)

    # Set the paging (this particular API call will only return up to 10 results at a time)
    paging = apicontractsv1.Paging()
    paging.limit = 10
    paging.offset = 1

    # Set the sorting
    sorting = apicontractsv1.CustomerPaymentProfileSorting()
    sorting.orderBy = apicontractsv1.CustomerPaymentProfileOrderFieldEnum.id
    sorting.orderDescending = "false"

    # Set search parameters
    search = apicontractsv1.CustomerPaymentProfileSearchTypeEnum.cardsExpiringInMonth
    month = "2019-12"

    # Creating the request with the required parameters
    request = apicontractsv1.getCustomerPaymentProfileListRequest()
    request.merchantAuthentication = merchant_auth
    request.refId = ref_id
    request.paging = paging
    request.sorting = sorting
    request.searchType = search
    request.month = month




    controller = getCustomerPaymentProfileListController(request)
    controller.setenvironment(AUTH_NET_ENVIRONMENT)
    controller.execute()

    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print ("SUCCESS")
            print ("Total Num in Result Set: %s" % response.totalNumInResultSet)
            print ("Result: {0}".format(response))
            for profile in response:              
                print(profile)

        else:
            print ("ERROR")
            if response.messages is not None:
                print ("Result code: %s" % response.messages.resultCode)
                print ("Message code: %s" % response.messages.message[0]['code'].text)
                print ("Message text: %s" % response.messages.message[0]['text'].text)
    return response


def get_customer_profile_transaction_list():
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = API_ID
    merchantAuth.transactionKey = TRANSACTION_KEY

    request = apicontractsv1.getTransactionListForCustomerRequest()
    request.merchantAuthentication = merchantAuth
    request.customerProfileId = "61644305564"

    controller = getTransactionListForCustomerController(request)
    controller.setenvironment(AUTH_NET_ENVIRONMENT)

    controller.execute()

    controller = transactionListForCustomerController.getresponse()

    if controller is not None:
        if controller.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print('Successfully got transaction list!')

            for transaction in controller.transactions.transaction:
                print('Transaction Id : %s' % transaction.transId)
                print('Transaction Status : %s' % transaction.transactionStatus)
                print('Amount Type : %s' % transaction.accountType)
                print('Settle Amount : %.2f' % transaction.settleAmount)
                print('Profile: {0}'.format(transaction.profile))

            if controller.messages is not None:
                print('Message Code : %s' % controller.messages.message[0]['code'].text)
                print('Message Text : %s' % controller.messages.message[0]['text'].text)
        else:
            if controller.messages is not None:
                print('Failed to get transaction list.\nCode:%s \nText:%s' % (controller.messages.message[0]['code'].text,controller.messages.message[0]['text'].text))

    return controller

def get_transaction_details(transId):
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = API_ID
    merchantAuth.transactionKey = TRANSACTION_KEY

    request = apicontractsv1.getTransactionDetailsRequest()
    request.merchantAuthentication = merchantAuth
    request.transId = str(transId)

    controller = getTransactionDetailsController(request)
    controller.setenvironment(AUTH_NET_ENVIRONMENT)
    controller.execute()

    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print('Successfully got transaction details!')

            print('Transaction Id : %s' % response.transaction.transId)
            print('Transaction Type : %s' % response.transaction.transactionType)
            print('Transaction Status : %s' % response.transaction.transactionStatus)
            print('Auth Amount : %.2f' % response.transaction.authAmount)
            print('Settle Amount : %.2f' % response.transaction.settleAmount)
            print('Card Type : %s' % response.transaction.payment.creditCard.cardType)

            pprint(vars(response.transaction))



            #namelist =list()

            #namelist.append(response.transaction.customer.email)
            #namelist.append(response.transaction.billTo.firstName)
            #namelist.append(response.transaction.billTo.lastName)

            #if response.transaction.customer.email in customers:   
            #    namelist.append(customers[response.transaction.customer.email][3])          
            #else:
            #    namelist.append('available')

            #outDict[namelist[0]] = namelist

            if hasattr(response.transaction, 'tax') == True:
                print('Tax : %s' % response.transaction.tax.amount)
            if hasattr(response.transaction, 'profile'):
                print('Customer Profile Id : %s' % response.transaction.profile.customerProfileId)

            if response.messages is not None:
                print('Message Code : %s' % response.messages.message[0]['code'].text)
                print('Message Text : %s' % response.messages.message[0]['text'].text)
        else:
            if response.messages is not None:
                print('Failed to get transaction details.\nCode:%s \nText:%s' % (response.messages.message[0]['code'].text,response.messages.message[0]['text'].text))

    return response

def get_transaction_list(batchId):
    """get transaction list for a specific batch"""
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = API_ID
    merchantAuth.transactionKey = TRANSACTION_KEY

    # set sorting parameters
    sorting = apicontractsv1.TransactionListSorting()
    sorting.orderBy = apicontractsv1.TransactionListOrderFieldEnum.id
    sorting.orderDescending = True

    # set paging and offset parameters
    paging = apicontractsv1.Paging()
    # Paging limit can be up to 1000 for this request
    paging.limit = 20
    paging.offset = 1

    request = apicontractsv1.getTransactionListRequest()
    request.merchantAuthentication = merchantAuth
    request.refId = "ref{}".format(int(time.time())*1000)
    request.batchId = str(batchId)
    request.sorting = sorting
    request.paging = paging

    controller = getTransactionListController(request)
    controller.setenvironment(AUTH_NET_ENVIRONMENT)
    controller.execute()

    # Work on the response
    response = controller.getresponse()

    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            if hasattr(response, 'transactions'):
                print('Successfully retrieved transaction list.')
                if response.messages is not None:
                    print('Message Code: %s' % response.messages.message[0]['code'].text)
                    print('Message Text: %s' % response.messages.message[0]['text'].text)
                    print('Total Number In Results: %s' % response.totalNumInResultSet)
                    print()
                for transaction in response.transactions.transaction:
                    print('Transaction Id: %s' % transaction.transId)
                    print('Transaction Status: %s' % transaction.transactionStatus)
                    if hasattr(transaction, 'accountType'):
                        print('Account Type: %s' % transaction.accountType)
                    print('Settle Amount: %.2f' % transaction.settleAmount)
                   
                    get_transaction_details(transaction.transId)
                    if hasattr(transaction, 'profile'):
                        print('Customer Profile ID: %s' % transaction.profile.customerProfileId)
                    print()
            else:
                if response.messages is not None:
                    print('Failed to get transaction list.')
                    print('Code: %s' % (response.messages.message[0]['code'].text))
                    print('Text: %s' % (response.messages.message[0]['text'].text))
        else:
            if response.messages is not None:
                print('Failed to get transaction list.')
                print('Code: %s' % (response.messages.message[0]['code'].text))
                print('Text: %s' % (response.messages.message[0]['text'].text))
    else:
        print('Error. No response received.')

    return response


def get_settled_batch_list(firstDate, lastDate):
    """get settled batch list"""
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = API_ID
    merchantAuth.transactionKey = TRANSACTION_KEY

    request = apicontractsv1.getSettledBatchListRequest()
    request.merchantAuthentication = merchantAuth
    request.refId = "ref{}".format(int(time.time())*1000)
    request.includeStatistics = True
    request.firstSettlementDate = firstDate
    request.lastSettlementDate = lastDate

    controller = getSettledBatchListController(request)
    controller.setenvironment(AUTH_NET_ENVIRONMENT)
    controller.execute()

    response = controller.getresponse()

    # Work on the response
    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            if hasattr(response, 'batchList'):
                print('Successfully retrieved batch list.')
                if response.messages is not None:
                    print('Message Code: %s' % response.messages.message[0]['code'].text)
                    print('Message Text: %s' % response.messages.message[0]['text'].text)
                    print()
                for batchEntry in response.batchList.batch:
                    print('Batch Id: %s' % batchEntry.batchId)
                    print('Settlement Time UTC: %s' % batchEntry.settlementTimeUTC)
                    print('Payment Method: %s' % batchEntry.paymentMethod)
                    if hasattr(batchEntry, 'marketType'):
                        print('Market Type: %s' % batchEntry.marketType)
                    if hasattr(batchEntry, 'product'):
                        print('Product: %s' % batchEntry.product)
                    if hasattr(batchEntry, 'statistics'):
                        if hasattr(batchEntry.statistics, 'statistic'):
                            for statistic in batchEntry.statistics.statistic:
                                if hasattr(statistic, 'accountType'):
                                    print('Account Type: %s' % statistic.accountType)
                                if hasattr(statistic, 'chargeAmount'):
                                    print('  Charge Amount: %.2f' % statistic.chargeAmount)
                                if hasattr(statistic, 'chargeCount'):
                                    print('  Charge Count: %s' % statistic.chargeCount)
                                if hasattr(statistic, 'refundAmount'):
                                    print('  Refund Amount: %.2f' % statistic.refundAmount)
                                if hasattr(statistic, 'refundCount'):
                                    print('  Refund Count: %s' % statistic.refundCount)
                                if hasattr(statistic, 'voidCount'):
                                    print('  Void Count: %s' % statistic.voidCount)
                                if hasattr(statistic, 'declineCount'):
                                    print('  Decline Count: %s' % statistic.declineCount)
                                if hasattr(statistic, 'errorCount'):
                                    print('  Error Count: %s' % statistic.errorCount)
                                if hasattr(statistic, 'returnedItemAmount'):
                                    print('  Returned Item Amount: %.2f' % statistic.returnedItemAmount)
                                if hasattr(statistic, 'returnedItemCount'):
                                    print('  Returned Item Count: %s' % statistic.returnedItemCount)
                                if hasattr(statistic, 'chargebackAmount'):
                                    print('  Chargeback Amount: %.2f' % statistic.chargebackAmount)
                                if hasattr(statistic, 'chargebackCount'):
                                    print('  Chargeback Count: %s' % statistic.chargebackCount)
                                if hasattr(statistic, 'correctionNoticeCount'):
                                    print('  Correction Notice Count: %s' % statistic.correctionNoticeCount)
                                if hasattr(statistic, 'chargeChargeBackAmount'):
                                    print('  Charge Chargeback Amount: %.2f' % statistic.chargeChargeBackAmount)
                                if hasattr(statistic, 'chargeChargeBackCount'):
                                    print('  Charge Chargeback Count: %s' % statistic.chargeChargeBackCount)
                                if hasattr(statistic, 'refundChargeBackAmount'):
                                    print('  Refund Chargeback Amount: %.2f' % statistic.refundChargeBackAmount)
                                if hasattr(statistic, 'refundChargeBackCount'):
                                    print('  Refund Chargeback Count: %s' % statistic.refundChargeBackCount)
                                if hasattr(statistic, 'chargeReturnedItemsAmount'):
                                    print('  Charge Returned Items Amount: %.2f' % statistic.chargeReturnedItemsAmount)
                                if hasattr(statistic, 'chargeReturnedItemsCount'):
                                    print('  Charge Returned Items Count: %s' % statistic.chargeReturnedItemsCount)
                                if hasattr(statistic, 'refundReturnedItemsAmount'):
                                    print('  Refund Returned Items Amount: %.2f' % statistic.refundReturnedItemsAmount)
                                if hasattr(statistic, 'refundReturnedItemsCount'):
                                    print('  Refund Returned Items Count: %s' % statistic.refundReturnedItemsCount)
                    print()

                    get_transaction_list(batchEntry.batchId)

            else:
                if response.messages is not None:
                    print('Failed to get transaction list.')
                    print('Code: %s' % (response.messages.message[0]['code'].text))
                    print('Text: %s' % (response.messages.message[0]['text'].text))
        else:
            if response.messages is not None:
                print('Failed to get transaction list.')
                print('Code: %s' % (response.messages.message[0]['code'].text))
                print('Text: %s' % (response.messages.message[0]['text'].text))
    else:
        print('Error. No response received.')

    return response


def get_customer_profile_ids():
    """get customer profile IDs"""
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = API_ID
    merchantAuth.transactionKey = TRANSACTION_KEY


    request = apicontractsv1.getCustomerProfileIdsRequest()
    request.merchantAuthentication = merchantAuth
    request.refId =  "ref{}".format(int(time.time())*1000)

    controller = getCustomerProfileIdsController(request)
    controller.setenvironment(AUTH_NET_ENVIRONMENT)
    controller.execute()

    # Work on the response
    response = controller.getresponse()

    # if (response.messages.resultCode == "Ok"):
    #     print("Successfully retrieved customer ids:")
    #     for identity in response.ids.numericString:
    #         print(identity)
    # else:
    #     print("response code: %s" % response.messages.resultCode)



    if response is not None:
        if response.messages.resultCode == apicontractsv1.messageTypeEnum.Ok:
            print ("SUCCESS")
            print ("Result: {0}".format(response))
            pprint(vars(response))
            if hasattr(response, 'ids'):
                if hasattr(response.ids, 'numericString'):
                    print('Successfully retrieved customer IDs.')
                    if response.messages is not None:
                        print('Message Code: %s' % response.messages.message[0]['code'].text)
                        print('Message Text: %s' % response.messages.message[0]['text'].text)
                        print('Total Number of IDs Returned in Results: %s'
                            % len(response.ids.numericString))
                        print()
                    # There's no paging options in this API request; the full list is returned every call.
                    # If the result set is going to be large, for this sample we'll break it down into smaller
                    # chunks so that we don't put 72,000 lines into a log file
                    print('First 20 results:')
                    for profileId in range(0,19):
                        print(response.ids.numericString[profileId])
            else:
                if response.messages is not None:
                    print('Failed to get list.')
                    print('Code: %s' % (response.messages.message[0]['code'].text))
                    print('Text: %s' % (response.messages.message[0]['text'].text))
        else:
            if response.messages is not None:
                print('Failed to get list.')
                print('Code: %s' % (response.messages.message[0]['code'].text))
                print('Text: %s' % (response.messages.message[0]['text'].text))
    else:
        print('Error. No response received.')

    return response

if(os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    #get_customer_profile_transaction_list()

    filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    print(filename);

    orders = util.loadcsv(sys.argv[1])

    #parser = argparse.ArgumentParser()
    #parser.add_argument('date')
    #args = parser.parse_args()

    #get_customer_payment_profile_list()
    #startDate = datetime.strptime(args.date, '%b %d %Y')
    #currentDate = datetime.now()

    #while startDate < currentDate:
    #    firstDate = startDate - timedelta(days=30)
    #    lastDate = startDate

    #    print("dates: {0} {1}".format(firstDate,lastDate))
    #    get_settled_batch_list(firstDate, lastDate)

    #   startDate += timedelta(days=30)
    #get_customer_profile_ids()
   
    outdict = dict();

    for key in orders:
        order = orders[key]
        print(order);
        card_type = "PayPal";
        order[5] = order[5].strip('\n');
        id = order[5];
        type = order[4];
        if ('Authorize.Net' in type):
            response = get_transaction_details(id);
            card_type = response.transaction.payment.creditCard.cardType;        

        order.append(card_type);

        #outdict[fields[0]] = fields;

    util.writecsv(filename + '.csv', orders);

    #util.ConvertToExcel(filename + '.csv')
    #util.writecsv('customers.csv', outDict)