import streamlit as st
from square.client import Client
import uuid

client = Client(
    access_token = "EAAAEPwzR3JBQOFbJ0aRaLdY3790IyM0hEl3xH78n0v1j11Yi2e-k0as_nxFTEPe",
    environment='sandbox'
)

with st.form("Add customer"):
   first_name = st.text_input('first name')
   last_name = st.text_input('last name')
   address_1 = st.text_input('address line 1')
   address_2 = st.text_input('address line 2')
   body = { 
    "idempotency_key": str(uuid.uuid4()),
    "given_name": first_name,
    "family_name": last_name,
    "address": {
  "address_line_1": address_1,
  "address_line_2": address_2
    }
    }
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        result = client.customers.create_customer(body)
        if result.is_success():
            st.write('success')
        else:
            st.write(result)

with st.form('Add payment'):
    custs= client.customers.list_customers()
    cust_list = []
    for i in range(len(custs.body['customers'])):
        print(custs.body['customers'][i]['given_name'])
        cust_list.append(custs.body['customers'][i]['given_name'])
    option = st.selectbox(
        "Customer Name",
        cust_list,
    )

    amt = st.text_input('amount')
    cur = st.selectbox('currency', ('AUD', 'USD'))
    
    cli_list=client.customers.search_customers(
  body = {}
    ).body['customers']

    for i in range(len(cli_list)):
        if option == cli_list[i]['given_name']:
            cust_id = cli_list[i]['id']

    body = {
    "source_id": "cnon:card-nonce-ok",
    "idempotency_key": str(uuid.uuid4()),
    "amount_money": {
      "amount": amt*100,
      "currency": cur
    },
    "customer_id": cust_id,
  }


    submitted = st.form_submit_button("Submit")
    if submitted:
        result = client.payments.create_payment(body)
        if result.is_success():
            st.write('success')
        else:
            st.write(result)

with st.form('View Payments'):
    submitted2 = st.form_submit_button('View Payments')
    if  submitted2:
        result = client.payments.list_payments().body['payments']
        for r in result:
            st.write(r['id'], r['amount_money'])