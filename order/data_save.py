# coding=utf-8
from order.models import *
import datetime
from django.utils.translation import gettext as _


def main():
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    order_info = Order.objects.filter(jointime__range=(today, tomorrow))
    for i in order_info:
        order_no = i.id
        delivery_no = i.delivery_no
        fact_money = str(i.fact_money)
        if i.customer:
            customer_id = i.customer.id
            customer_name = _(i.customer.name)
            customer_sex = i.customer.sex
        else:
            customer_id = None
            customer_name = None
            customer_sex = False
        if i.customer.level:
            customer_level = i.customer.level.level
            customer_level_name = _(i.customer.level.name)
        else:
            customer_level = 1
            customer_level_name = _("基本等级")
        if i.customer.user:
            user_username = i.customer.user.username
            user_first_name = _(i.customer.user.first_name)
            user_group_name = _(i.customer.user.groups.all()[0].name)
        else:
            user_username = None
            user_first_name = None
            user_group_name = None
        if i.customer.get_contact_info():
            address = _(i.customer.get_contact_info()[0].address)
            phone_number = i.customer.get_contact_info()[0].phone_number
        else:
            address = None
            phone_number = None
        if i.issuing_person:
            issuing_person = _(i.issuing_person.name)
        else:
            issuing_person = None
        if i.product:
            product_name = _(i.product.name)
            product_price = str(i.product.price)
            product_delivery_type = _(i.product.delivery_type)
        else:
            product_delivery_type = None
            product_name = None
            product_price = None
        if i.state:
            state_name = _(i.state.name)
            state_level = int(i.state.level)
        else:
            state_level = None
            state_name = None
        remark = i.remark
        jointime = i.jointime.strftime('%Y-%m-%d %H:%M:%S')

        order_save = Order_all_info(order_no=order_no,
                                    delivery_no=delivery_no,
                                    fact_money=fact_money,
                                    customer_id=customer_id,
                                    customer_name=customer_name,
                                    customer_sex=customer_sex,
                                    customer_level=customer_level,
                                    customer_level_name=customer_level_name,
                                    user_username=user_username,
                                    user_first_name=user_first_name,
                                    user_group_name=user_group_name,
                                    address=address,
                                    phone_number=phone_number,
                                    issuing_person=issuing_person,
                                    product_name=product_name,
                                    product_price=product_price,
                                    product_delivery_type=product_delivery_type,
                                    state_name=state_name,
                                    state_level=state_level,
                                    remark=remark,
                                    jointime=jointime)
        order_save.save()


main()