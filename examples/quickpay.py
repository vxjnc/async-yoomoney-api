import asyncio
from AsyncYoomoney import Quickpay

quickpay = asyncio.run(Quickpay.create(
    receiver="410019014512803",
    quickpay_form="shop",
    targets="Sponsor this project",
    paymentType="SB",
    sum=150,
))

print(quickpay.base_url)
print(quickpay.redirected_url)
