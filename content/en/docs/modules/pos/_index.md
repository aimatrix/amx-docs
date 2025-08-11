---
title: "Point of Sales (POS)"
linkTitle: "POS"
weight: 10
description: >
  Complete point of sales solution for retail and hospitality businesses
---

# Point of Sales (POS) Module

## Overview

The BigLedger Point of Sales (POS) module is a comprehensive retail management solution designed for modern businesses. Built with speed, reliability, and user-friendliness in mind, it seamlessly integrates with all other BigLedger modules while providing standalone capabilities for retail operations.

## Key Features

### 🚀 Core Functionality

- **Multi-Store Support**: Manage multiple locations from a single system
- **Offline Mode**: Continue operations even without internet connectivity
- **Touch-Optimized Interface**: Designed for tablets and touch screens
- **Barcode Scanning**: Support for 1D and 2D barcodes
- **Quick Keys**: Customizable product shortcuts
- **Multi-Payment Methods**: Cash, card, digital wallets, layaway
- **Real-time Inventory**: Instant stock updates across all channels
- **Customer Management**: Built-in CRM and loyalty programs
- **Multi-Currency**: Accept payments in multiple currencies
- **Tax Management**: Complex tax calculations and reporting

### 💳 Payment Processing

#### Supported Payment Methods
- Cash (with cash drawer integration)
- Credit/Debit Cards (EMV, NFC, Swipe)
- Digital Wallets (Apple Pay, Google Pay, Samsung Pay)
- QR Code Payments (Alipay, WeChat Pay)
- Store Credit and Gift Cards
- Layaway and Installments
- Buy Now, Pay Later (BNPL) Integration
- Cryptocurrency (Bitcoin, Ethereum, USDC)

#### Payment Gateway Integrations
- Stripe
- Square
- PayPal
- Adyen
- Worldpay
- Regional gateways (country-specific)

### 📊 Sales Features

- **Product Variants**: Size, color, style management
- **Bundle Products**: Create and sell product bundles
- **Promotions Engine**: 
  - Buy X Get Y
  - Percentage/Fixed discounts
  - Time-based promotions
  - Member-exclusive deals
  - Coupon codes
- **Price Management**:
  - Multiple price lists
  - Customer-specific pricing
  - Volume discounts
  - Dynamic pricing rules
- **Commission Tracking**: Sales associate commissions
- **Returns & Exchanges**: Full or partial returns with reason tracking
- **Quotations**: Create and convert quotes to sales
- **Suspended Sales**: Park and retrieve transactions

### 👥 Customer Experience

- **Customer Display**: Secondary display for customers
- **Digital Receipts**: Email/SMS receipts
- **Loyalty Programs**:
  - Points-based rewards
  - Tier-based benefits
  - Punch cards
  - Cashback programs
- **Customer Account**: Store credit, payment history
- **Wishlist Management**: Save items for later
- **Order Management**: Special orders, pre-orders
- **Appointment Booking**: For service-based businesses

### 🏪 Store Operations

- **Shift Management**: Open/close shifts with cash reconciliation
- **Cash Management**:
  - Cash float
  - Cash in/out
  - Till reconciliation
  - Safe drops
- **Staff Management**:
  - Role-based permissions
  - Time clock integration
  - Performance tracking
  - Training mode
- **Inventory Operations**:
  - Stock transfers
  - Stock counts
  - Receiving
  - Adjustments

## Industry-Specific Features

### Retail
- Size/color matrix
- Season management
- Style tracking
- Vendor catalogs
- Purchase orders

### Restaurant & Hospitality
- Table management
- Kitchen display system
- Menu modifiers
- Split bills
- Tips management
- Happy hour pricing
- Course management

### Services
- Appointment scheduling
- Service duration tracking
- Resource allocation
- Package sales
- Membership management

## Hardware Integration

### Supported Hardware

#### Receipt Printers
- Epson TM series
- Star Micronics
- Bixolon
- Citizen
- Bluetooth mobile printers

#### Barcode Scanners
- USB scanners (plug-and-play)
- Bluetooth scanners
- 2D imaging scanners
- Mobile device cameras

#### Payment Terminals
- Ingenico
- Verifone
- PAX
- Clover
- Square Terminal

#### Cash Drawers
- USB-triggered drawers
- Printer-triggered drawers
- Manual drawers with sensors

#### Scales
- Digital weighing scales
- Label printing scales
- Counting scales

#### Other Devices
- Customer displays
- Pole displays
- Kitchen printers
- RFID readers
- Fingerprint scanners

## Configuration Guide

### Initial Setup

#### Step 1: Store Configuration

```yaml
Store Settings:
  Name: Main Store
  Code: MAIN
  Address: 123 Business St
  Tax ID: XX-XXXXXXX
  Currency: USD
  Time Zone: America/New_York
  
Operating Hours:
  Monday-Friday: 9:00 AM - 9:00 PM
  Saturday: 10:00 AM - 8:00 PM
  Sunday: 11:00 AM - 6:00 PM
```

#### Step 2: Register Setup

```yaml
Register Configuration:
  Register Name: Register 1
  Register Code: REG001
  Location: Front Counter
  Receipt Printer: Epson TM-T88V
  Cash Drawer: Auto-open
  Scanner: USB Barcode Scanner
  Payment Terminal: Integrated
```

#### Step 3: User Permissions

| Role | Permissions |
|------|------------|
| Manager | All permissions |
| Supervisor | Sales, returns, reports, cash management |
| Cashier | Sales, returns, view reports |
| Trainee | Sales only (training mode) |

### Payment Configuration

#### Credit Card Setup

1. Navigate to **POS → Settings → Payment Methods**
2. Select payment gateway (e.g., Stripe)
3. Enter API credentials
4. Configure terminal settings
5. Test connection

#### Tax Configuration

```javascript
// Tax Rules Example
{
  "default_tax": {
    "rate": 0.08,
    "name": "State Tax",
    "type": "percentage"
  },
  "tax_rules": [
    {
      "category": "food",
      "rate": 0,
      "name": "Food Exempt"
    },
    {
      "category": "luxury",
      "rate": 0.12,
      "name": "Luxury Tax"
    }
  ]
}
```

## Operations Guide

### Daily Operations

#### Opening Procedures

1. **Start Shift**
   - Log into POS system
   - Count opening cash float
   - Enter float amount
   - Verify hardware connections
   - Print test receipt

2. **Verify Inventory**
   - Check stock levels
   - Review low stock alerts
   - Process pending transfers

#### During Operations

1. **Processing Sales**
   ```
   1. Scan/search products
   2. Apply discounts if applicable
   3. Select payment method
   4. Process payment
   5. Print/email receipt
   ```

2. **Handling Returns**
   ```
   1. Scan receipt or search transaction
   2. Select items to return
   3. Enter return reason
   4. Process refund
   5. Update inventory
   ```

#### Closing Procedures

1. **End Shift**
   - Count cash drawer
   - Reconcile payments
   - Generate Z-report
   - Secure cash in safe
   - Clock out

### Reports & Analytics

#### Sales Reports
- Daily sales summary
- Hourly sales analysis
- Product performance
- Category analysis
- Staff performance
- Payment method breakdown

#### Inventory Reports
- Stock levels
- Movement reports
- Shrinkage analysis
- Reorder suggestions

#### Customer Reports
- Top customers
- Customer purchase history
- Loyalty program metrics
- Customer lifetime value

## Integration Guide

### E-Commerce Integration

```python
# Sync online and offline inventory
def sync_inventory():
    online_stock = get_ecommerce_stock()
    pos_stock = get_pos_stock()
    
    synchronized_stock = reconcile_stock(online_stock, pos_stock)
    
    update_all_channels(synchronized_stock)
    return synchronized_stock
```

### Accounting Integration

The POS module automatically syncs with Financial Accounting:
- Sales recorded as revenue
- Tax collected tracked separately
- Cash reconciliation to bank accounts
- Inventory COGS calculations
- Commission accruals

### CRM Integration

Customer data flows seamlessly to CRM:
- Purchase history
- Preferences
- Contact information
- Loyalty status
- Marketing consent

## Best Practices

### Performance Optimization

1. **Database Optimization**
   - Regular index maintenance
   - Archive old transactions
   - Optimize product search

2. **Network Optimization**
   - Local caching for offline mode
   - Compressed data transmission
   - Prioritized transaction queuing

3. **Hardware Maintenance**
   - Regular cleaning of scanners
   - Printer maintenance
   - Cash drawer calibration

### Security Best Practices

1. **Access Control**
   - Strong password policies
   - Two-factor authentication
   - Regular permission audits
   - Session timeouts

2. **PCI Compliance**
   - Never store card details
   - Use tokenization
   - Regular security updates
   - Encrypted communications

3. **Cash Management**
   - Regular cash drops
   - Dual control for large amounts
   - Security cameras
   - Audit trails

### Training Guidelines

#### New Cashier Training

**Week 1: Basics**
- System navigation
- Product search
- Basic sales transactions
- Payment processing

**Week 2: Advanced**
- Returns and exchanges
- Discounts and promotions
- Customer management
- Special orders

**Week 3: Operations**
- Opening/closing procedures
- Cash management
- Report generation
- Troubleshooting

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Scanner not working | Check USB connection, reinstall drivers |
| Printer offline | Verify power, check paper, reset spooler |
| Payment declined | Check internet, verify terminal connection |
| Slow performance | Clear cache, check network, optimize database |
| Sync issues | Check connectivity, force sync, review logs |

### Error Codes

- **POS001**: Network connection lost
- **POS002**: Payment gateway timeout
- **POS003**: Insufficient inventory
- **POS004**: Invalid barcode
- **POS005**: Printer error

## API Reference

### REST API Endpoints

```http
# Create Sale
POST /api/v1/pos/sales
Content-Type: application/json

{
  "store_id": "STORE001",
  "register_id": "REG001",
  "items": [
    {
      "product_id": "PROD123",
      "quantity": 2,
      "price": 29.99
    }
  ],
  "payment": {
    "method": "card",
    "amount": 59.98
  }
}

# Get Sales Report
GET /api/v1/pos/reports/sales?date=2024-01-01&store_id=STORE001

# Process Return
POST /api/v1/pos/returns
{
  "original_sale_id": "SALE123",
  "items": ["ITEM1", "ITEM2"],
  "reason": "defective"
}
```

### Webhooks

```javascript
// Available webhook events
{
  "sale.completed": "Triggered when sale is finalized",
  "return.processed": "Triggered when return is completed",
  "shift.closed": "Triggered at shift end",
  "inventory.low": "Triggered when stock below threshold"
}
```

## Mobile POS

### Features
- Full POS functionality on tablets
- Line busting capabilities
- Mobile payments
- Inventory lookup
- Customer assistance mode

### Supported Devices
- iOS: iPad (iOS 13+)
- Android: Tablets (Android 8+)
- Windows: Surface devices

## Updates & Roadmap

### Recent Updates (v1.0)
- ✅ Offline mode improvements
- ✅ Advanced promotions engine
- ✅ Multi-currency support
- ✅ Kitchen display system
- ✅ BNPL integration

### Upcoming Features (v1.1)
- 🔄 AI-powered demand forecasting
- 🔄 Self-checkout support
- 🔄 Augmented reality product preview
- 🔄 Voice-activated commands
- 🔄 Blockchain-based loyalty points

## Support Resources

- 📖 [Video Tutorials](/tutorials/pos/)
- 💬 [Community Forum](https://forum.bigledger.com/pos)
- 📧 [Email Support](mailto:pos-support@bigledger.com)
- 📞 24/7 Support: +1-800-POS-HELP

---

*The BigLedger POS module - Empowering retail excellence through technology.*