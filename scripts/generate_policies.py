"""
Generate realistic e-commerce store policies
"""
import os

DATA_DIR = "data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

POLICIES = {
    "return_policy.md": """# Return Policy

## Overview
At ShopAssist, we want you to be completely satisfied with your purchase. If you're not happy with your order, we're here to help.

## Return Window
- **Electronics**: 30 days from delivery date
- **Opened electronics**: 15 days with 15% restocking fee
- **Damaged or defective items**: 90 days, full refund

## Return Process
1. Log into your account and go to "Order History"
2. Select the item you wish to return
3. Choose your reason for return
4. Print the prepaid return label
5. Package the item securely with all original accessories
6. Drop off at any authorized shipping location

## Conditions
- Items must be in original packaging when possible
- All accessories, manuals, and parts must be included
- Serial numbers must match the original purchase
- Items showing signs of use beyond testing may incur restocking fees

## Refund Timeline
- Refunds are processed within 5-7 business days after we receive your return
- Original payment method will be credited
- Shipping costs are non-refundable unless item was damaged/defective

## Non-Returnable Items
- Downloadable software products
- Gift cards
- Items marked as "Final Sale"
- Products without serial numbers or with damaged UPC codes
""",

    "shipping_policy.md": """# Shipping Policy

## Shipping Options

### Standard Shipping
- **Cost**: Free on orders over $50, otherwise $5.99
- **Delivery**: 5-7 business days
- **Tracking**: Provided via email

### Expedited Shipping
- **Cost**: $12.99
- **Delivery**: 2-3 business days
- **Tracking**: Real-time tracking available

### Express Shipping
- **Cost**: $24.99
- **Delivery**: Next business day (orders placed before 2 PM)
- **Tracking**: Real-time tracking with SMS updates

## Processing Time
- Most orders ship within 1-2 business days
- Custom or made-to-order items may take 3-5 business days
- You'll receive a confirmation email when your order ships

## International Shipping
- Available to select countries
- Costs calculated at checkout
- Customs duties and taxes are the responsibility of the recipient
- Delivery times vary by destination (7-21 business days)

## Order Tracking
- Track your order at www.shopassist.com/track
- Tracking information updates every 24 hours
- Contact customer service if tracking hasn't updated in 48 hours

## Shipping Restrictions
- We cannot ship to P.O. boxes for certain large items
- Some products cannot be shipped to Alaska, Hawaii, or international locations
- Age verification required for certain electronics at delivery
""",

    "warranty_info.md": """# Warranty Information

## Manufacturer Warranty
All products sold on ShopAssist come with the manufacturer's standard warranty. Warranty terms vary by brand and product type.

## Standard Warranty Coverage
- **Laptops & Computers**: 1 year parts and labor
- **Smartphones & Tablets**: 1 year limited warranty
- **Cameras & Audio**: 1-2 years depending on brand
- **Accessories**: 90 days to 1 year

## What's Covered
- Manufacturing defects in materials or workmanship
- Hardware failures under normal use
- Defective parts replacement

## What's NOT Covered
- Accidental damage (drops, spills, cracks)
- Normal wear and tear
- Software issues or viruses
- Unauthorized repairs or modifications
- Cosmetic damage that doesn't affect functionality
- Loss or theft

## Extended Protection Plans
We offer optional extended protection plans:

### Standard Protection (2 years)
- **Cost**: 10-15% of product price
- Coverage for mechanical/electrical failures
- Free shipping for repairs

### Premium Protection (3 years)
- **Cost**: 15-20% of product price
- Everything in Standard, plus:
- Accidental damage protection (2 claims)
- Battery replacement coverage
- 24/7 customer support

## Filing a Warranty Claim
1. Contact manufacturer customer service (number on warranty card)
2. Provide proof of purchase and serial number
3. Describe the issue and any troubleshooting done
4. Ship to designated repair center if required
5. Typical repair turnaround: 7-14 business days

## ShopAssist Support
While we don't directly service warranty claims, our team can:
- Help you contact the right manufacturer
- Verify your warranty status
- Assist with extended protection plan claims
- Facilitate returns during the initial 30-day period
""",

    "payment_methods.md": """# Payment Methods

## Accepted Payment Types

### Credit & Debit Cards
We accept:
- Visa
- Mastercard
- American Express
- Discover
- All major debit cards with Visa/MC logo

### Digital Wallets
- PayPal
- Apple Pay
- Google Pay
- Shop Pay

### Other Options
- ShopAssist Gift Cards
- Store Credit from returns
- Buy Now, Pay Later (Affirm, Klarna, Afterpay)

## Payment Security
- All transactions use 256-bit SSL encryption
- PCI DSS Level 1 compliant
- We never store complete credit card information
- 3D Secure authentication for added protection

## Buy Now, Pay Later

### Affirm
- Split purchases into 3, 6, or 12 monthly payments
- Available on orders $50-$17,500
- Instant approval decision
- 0-30% APR based on credit

### Klarna
- Pay in 4 interest-free payments
- Available on orders $35-$1,000
- Automatic payments every 2 weeks
- No interest if paid on time

### Afterpay
- Pay in 4 interest-free installments
- Available on orders $35-$1,000
- First payment at purchase, then every 2 weeks
- Late fees apply for missed payments

## Gift Cards
- Available in denominations from $10-$500
- Never expire
- Can be used with other payment methods
- Check balance at www.shopassist.com/giftcard

## Billing Information
- Billing address must match payment method
- International cards accepted (subject to conversion fees)
- Authorization hold placed at time of order
- Charge processed when order ships

## Payment Issues
If your payment is declined:
- Verify billing information matches your card
- Check with your bank for authorization
- Try a different payment method
- Contact customer service for assistance
""",

    "faq.md": """# Frequently Asked Questions

## Orders & Shopping

**Q: How do I track my order?**
A: Once your order ships, you'll receive a tracking number via email. You can also track orders by logging into your account and visiting "Order History."

**Q: Can I change or cancel my order?**
A: Orders can be modified or cancelled within 1 hour of placement. After that, the order is sent to our warehouse and cannot be changed. Contact customer service immediately if you need help.

**Q: Do you price match?**
A: We offer a 14-day price match guarantee on identical items from authorized retailers. Contact customer service with proof of the lower price.

**Q: What if an item is out of stock?**
A: Out of stock items show estimated restock dates. You can sign up for email notifications when the item becomes available.

## Returns & Refunds

**Q: How long do I have to return an item?**
A: Most items can be returned within 30 days. Electronics have specific return windows - see our Return Policy for details.

**Q: How long does a refund take?**
A: Refunds are processed within 5-7 business days after we receive your return. It may take an additional 3-5 days for the credit to appear on your statement.

**Q: Can I exchange an item?**
A: We don't offer direct exchanges. Return the original item for a refund and place a new order for the desired item.

## Shipping

**Q: Do you offer free shipping?**
A: Yes! Orders over $50 qualify for free standard shipping.

**Q: Can I ship to multiple addresses?**
A: Currently, each order can only ship to one address. Place separate orders for different shipping addresses.

**Q: Do you ship internationally?**
A: We ship to select international countries. Shipping costs and delivery times vary by destination.

## Products & Warranties

**Q: Are your products authentic?**
A: Yes, we only sell authentic products from authorized distributors and manufacturers.

**Q: Do products come with warranties?**
A: All products include the manufacturer's standard warranty. Extended protection plans are available at checkout.

**Q: Can I purchase a warranty after my order?**
A: Extended protection plans must be purchased within 30 days of your original order.

## Account & Support

**Q: Do I need an account to shop?**
A: No, but creating an account makes checkout faster and allows you to track orders and save payment methods.

**Q: How do I reset my password?**
A: Click "Forgot Password" on the login page. You'll receive an email with reset instructions.

**Q: How can I contact customer service?**
A: 
- Email: support@shopassist.com (24-48 hour response)
- Phone: 1-800-SHOP-RAG (24/7)
- Live Chat: Available on our website 9 AM - 9 PM EST
"""
}

def main():
    print("=" * 60)
    print("Generating Store Policies")
    print("=" * 60)
    
    for filename, content in POLICIES.items():
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Created {filename}")
    
    print("\n" + "=" * 60)
    print("✓ All policies generated!")
    print("=" * 60)

if __name__ == "__main__":
    main()