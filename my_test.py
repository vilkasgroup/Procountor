from procountor.client import Client


client = Client(
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyNzU4NCIsImF1ZCI6InZpbGthc1Rlc3RDbGllbnQiLCJpc3MiOiJodHRwczovL2FwaS10ZXN0LnByb2NvdW50b3IuY29tIiwiaWF0IjoxNjA1MjcyMDk5LCJqdGkiOiJkOTY2ZWM2My0wNTRkLTQzMmYtODRhNC0zM2NkOTVjN2VjYTAiLCJjaWQiOjE0NDM4fQ.wXmND7bdWR8X077oeXz_C-yKa46CUl3xxt_jE9-WhWk",
    "vilkasTestClient",
    "testsecret_NH6xoz6GHo5oHWt2orJZ",
    "",
    True,
    "20.08"
)

moo = {
        'startDate': '2000-01-01',
        'endDate': '2020-12-31',
}

response = client.get_invoices(**moo)

print(response)