---
title: "API Reference"
linkTitle: "API Reference"
weight: 30
menu:
  main:
    weight: 30
description: >
  Complete API documentation for BigLedger platform integration
---

# BigLedger API Reference

## Overview

The BigLedger API provides programmatic access to all platform functionality through RESTful endpoints and GraphQL queries. Built with developers in mind, our API offers comprehensive access to every feature available in the BigLedger platform.

## Key Features

- **RESTful Design**: Predictable resource-oriented URLs
- **GraphQL Support**: Flexible queries for exactly the data you need
- **Real-time Updates**: WebSocket connections for live data
- **Comprehensive Coverage**: Every UI action available via API
- **Multi-tenant**: Full isolation between tenant data
- **Versioning**: Backward-compatible API versions
- **Rate Limiting**: Fair usage policies with generous limits
- **Authentication**: OAuth 2.0, API keys, and JWT tokens

## Getting Started

### Base URLs

```
Production: https://api.bigledger.com/v1
Staging:    https://api-staging.bigledger.com/v1
Sandbox:    https://api-sandbox.bigledger.com/v1
GraphQL:    https://graphql.bigledger.com/v1
WebSocket:  wss://ws.bigledger.com/v1
```

### Authentication

BigLedger supports multiple authentication methods:

#### API Key Authentication

```bash
curl -X GET https://api.bigledger.com/v1/accounts \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### OAuth 2.0

```javascript
// OAuth 2.0 flow
const oauth = {
  client_id: 'YOUR_CLIENT_ID',
  client_secret: 'YOUR_CLIENT_SECRET',
  redirect_uri: 'https://yourapp.com/callback',
  scope: 'read write',
  grant_type: 'authorization_code'
};

// 1. Redirect user to authorize
window.location = `https://auth.bigledger.com/oauth/authorize?
  client_id=${oauth.client_id}&
  redirect_uri=${oauth.redirect_uri}&
  response_type=code&
  scope=${oauth.scope}`;

// 2. Exchange code for token
const response = await fetch('https://auth.bigledger.com/oauth/token', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    grant_type: 'authorization_code',
    code: authorizationCode,
    client_id: oauth.client_id,
    client_secret: oauth.client_secret,
    redirect_uri: oauth.redirect_uri
  })
});

const { access_token, refresh_token } = await response.json();
```

#### JWT Authentication

```python
import jwt
import requests
from datetime import datetime, timedelta

# Generate JWT
payload = {
    'sub': 'user_id',
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, 'YOUR_SECRET_KEY', algorithm='HS256')

# Make authenticated request
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://api.bigledger.com/v1/accounts', headers=headers)
```

### Rate Limits

| Plan | Requests/Hour | Burst Rate | Concurrent |
|------|--------------|------------|------------|
| Free | 1,000 | 10/sec | 5 |
| Starter | 10,000 | 50/sec | 20 |
| Professional | 100,000 | 200/sec | 100 |
| Enterprise | Unlimited | Custom | Custom |

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Core Resources

### Accounts

#### Get All Accounts

```http
GET /api/v1/accounts
```

Query Parameters:
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20, max: 100)
- `type` (string): Filter by account type
- `status` (string): Filter by status (active, inactive)
- `search` (string): Search accounts by name or code

Response:
```json
{
  "data": [
    {
      "id": "acc_1234567890",
      "code": "1000",
      "name": "Cash",
      "type": "asset",
      "subtype": "current_asset",
      "currency": "USD",
      "balance": 50000.00,
      "normal_balance": "debit",
      "description": "Cash and cash equivalents",
      "is_active": true,
      "is_reconcilable": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

#### Create Account

```http
POST /api/v1/accounts
Content-Type: application/json

{
  "code": "1001",
  "name": "Petty Cash",
  "type": "asset",
  "subtype": "current_asset",
  "currency": "USD",
  "opening_balance": 1000.00,
  "description": "Petty cash fund"
}
```

### Transactions

#### Create Journal Entry

```http
POST /api/v1/journal-entries
Content-Type: application/json

{
  "date": "2024-01-15",
  "reference": "JE-2024-001",
  "description": "Monthly rent payment",
  "lines": [
    {
      "account_id": "acc_6100",
      "debit": 5000.00,
      "credit": 0,
      "description": "Rent expense"
    },
    {
      "account_id": "acc_1000",
      "debit": 0,
      "credit": 5000.00,
      "description": "Cash payment"
    }
  ],
  "attachments": ["doc_abc123"]
}
```

Response:
```json
{
  "id": "je_987654321",
  "number": "JE-2024-001",
  "date": "2024-01-15",
  "status": "posted",
  "total_debit": 5000.00,
  "total_credit": 5000.00,
  "is_balanced": true,
  "created_by": "user_123",
  "created_at": "2024-01-15T14:30:00Z",
  "lines": [
    {
      "id": "jel_111",
      "account": {
        "id": "acc_6100",
        "code": "6100",
        "name": "Rent Expense"
      },
      "debit": 5000.00,
      "credit": 0,
      "description": "Rent expense"
    },
    {
      "id": "jel_112",
      "account": {
        "id": "acc_1000",
        "code": "1000",
        "name": "Cash"
      },
      "debit": 0,
      "credit": 5000.00,
      "description": "Cash payment"
    }
  ]
}
```

### Invoices

#### Create Invoice

```http
POST /api/v1/invoices
Content-Type: application/json

{
  "customer_id": "cust_123456",
  "invoice_date": "2024-01-15",
  "due_date": "2024-02-15",
  "currency": "USD",
  "lines": [
    {
      "product_id": "prod_789",
      "description": "Consulting Services",
      "quantity": 10,
      "unit_price": 150.00,
      "tax_rate": 0.08,
      "discount_percentage": 10
    }
  ],
  "payment_terms": "net_30",
  "notes": "Thank you for your business"
}
```

### Customers

#### Customer Object

```json
{
  "id": "cust_123456",
  "name": "Acme Corporation",
  "email": "accounts@acme.com",
  "phone": "+1-555-0100",
  "website": "https://acme.com",
  "tax_id": "12-3456789",
  "currency": "USD",
  "payment_terms": "net_30",
  "credit_limit": 50000.00,
  "balance": 12500.00,
  "status": "active",
  "billing_address": {
    "line1": "123 Main Street",
    "line2": "Suite 100",
    "city": "San Francisco",
    "state": "CA",
    "postal_code": "94105",
    "country": "US"
  },
  "shipping_addresses": [...],
  "contacts": [...],
  "custom_fields": {
    "industry": "Technology",
    "employee_count": "100-500"
  }
}
```

## GraphQL API

### Schema

```graphql
type Query {
  account(id: ID!): Account
  accounts(filter: AccountFilter, page: Int, limit: Int): AccountConnection
  invoice(id: ID!): Invoice
  invoices(filter: InvoiceFilter, page: Int, limit: Int): InvoiceConnection
  customer(id: ID!): Customer
  customers(filter: CustomerFilter, page: Int, limit: Int): CustomerConnection
  reports(type: ReportType!, params: ReportParams): Report
}

type Mutation {
  createAccount(input: CreateAccountInput!): Account
  updateAccount(id: ID!, input: UpdateAccountInput!): Account
  deleteAccount(id: ID!): DeleteResult
  
  createInvoice(input: CreateInvoiceInput!): Invoice
  sendInvoice(id: ID!): Invoice
  voidInvoice(id: ID!, reason: String!): Invoice
  
  createPayment(input: CreatePaymentInput!): Payment
  applyPayment(paymentId: ID!, invoiceId: ID!): PaymentApplication
}

type Subscription {
  accountUpdated(id: ID!): Account
  invoiceCreated: Invoice
  paymentReceived: Payment
}
```

### Example Queries

#### Get Customer with Invoices

```graphql
query GetCustomerWithInvoices($customerId: ID!) {
  customer(id: $customerId) {
    id
    name
    email
    balance
    invoices(status: UNPAID) {
      edges {
        node {
          id
          number
          date
          dueDate
          total
          amountDue
          status
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

#### Create and Send Invoice

```graphql
mutation CreateAndSendInvoice($input: CreateInvoiceInput!) {
  createInvoice(input: $input) {
    id
    number
    total
    status
  }
  
  sendInvoice(id: $invoiceId) {
    id
    status
    sentAt
  }
}
```

## Webhooks

### Available Events

```json
{
  "account.created": "New account created",
  "account.updated": "Account details updated",
  "account.deleted": "Account deleted",
  
  "invoice.created": "New invoice created",
  "invoice.sent": "Invoice sent to customer",
  "invoice.paid": "Invoice fully paid",
  "invoice.overdue": "Invoice is overdue",
  
  "payment.received": "Payment received",
  "payment.failed": "Payment failed",
  "payment.refunded": "Payment refunded",
  
  "customer.created": "New customer created",
  "customer.updated": "Customer details updated",
  "customer.credit_limit_exceeded": "Customer exceeded credit limit"
}
```

### Webhook Payload

```json
{
  "id": "evt_1234567890",
  "type": "invoice.paid",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "invoice": {
      "id": "inv_987654321",
      "number": "INV-2024-001",
      "customer_id": "cust_123456",
      "total": 1500.00,
      "amount_paid": 1500.00,
      "paid_at": "2024-01-15T10:30:00Z"
    }
  },
  "signature": "sha256=abcdef123456..."
}
```

### Webhook Security

Verify webhook signatures:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(
        f"sha256={expected}",
        signature
    )
```

## SDK & Libraries

### Official SDKs

- **JavaScript/TypeScript**: `npm install @bigledger/sdk`
- **Python**: `pip install bigledger`
- **Ruby**: `gem install bigledger`
- **PHP**: `composer require bigledger/sdk`
- **Go**: `go get github.com/bigledger/go-sdk`
- **Java**: Maven/Gradle available
- **.NET**: `dotnet add package BigLedger.SDK`

### JavaScript SDK Example

```javascript
import { BigLedger } from '@bigledger/sdk';

const client = new BigLedger({
  apiKey: 'YOUR_API_KEY',
  environment: 'production'
});

// Create customer
const customer = await client.customers.create({
  name: 'New Customer',
  email: 'customer@example.com'
});

// Create invoice
const invoice = await client.invoices.create({
  customerId: customer.id,
  lines: [
    {
      description: 'Service',
      quantity: 1,
      unitPrice: 100.00
    }
  ]
});

// Send invoice
await client.invoices.send(invoice.id);

// Listen for webhook events
client.webhooks.on('payment.received', (event) => {
  console.log('Payment received:', event.data);
});
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "request_id": "req_abc123",
    "documentation_url": "https://docs.bigledger.com/api/errors#VALIDATION_ERROR"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|------------|-------------|
| `AUTHENTICATION_FAILED` | 401 | Invalid or missing authentication |
| `PERMISSION_DENIED` | 403 | Insufficient permissions |
| `RESOURCE_NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

## Testing

### Sandbox Environment

The sandbox environment provides:
- Full API functionality
- Test data generation
- Webhook testing
- No charges or real transactions
- Data reset every 24 hours

### Test Credit Cards

| Number | Type | Result |
|--------|------|--------|
| 4242 4242 4242 4242 | Visa | Success |
| 4000 0000 0000 0002 | Visa | Declined |
| 4000 0000 0000 9995 | Visa | Insufficient funds |

### Postman Collection

Download our Postman collection:
[BigLedger API Collection](https://www.postman.com/bigledger/workspace/bigledger-api/collection)

## API Changelog

### Version 1.0.2 (2024-01-15)
- Added bulk operations for invoices
- Improved webhook retry logic
- New endpoint for tax calculations

### Version 1.0.1 (2023-12-01)
- GraphQL subscriptions support
- Enhanced filtering options
- Performance improvements

### Version 1.0.0 (2023-10-01)
- Initial public release
- RESTful API
- GraphQL API
- Webhook system

## Support

- 📖 [API Documentation](https://docs.bigledger.com/api)
- 💬 [Developer Forum](https://forum.bigledger.com/developers)
- 📧 [API Support](mailto:api@bigledger.com)
- 🐛 [Report Issues](https://github.com/bigledger/api/issues)

---

*Build powerful integrations with the BigLedger API platform.*