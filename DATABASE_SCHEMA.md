# Lost & Found Portal - Database Schema

## 📊 Database Overview

The system uses **4 main tables** with **76 total records** across all tables.

---

## 🗄️ Table Details

### 1. **accounts_customuser** (User Management)
**Purpose**: Stores all user accounts (normal users and administrators)

| Field Name | Type | Description |
|------------|------|-------------|
| `id` | BigAutoField | Primary key |
| `password` | CharField | Hashed password |
| `last_login` | DateTimeField | Last login timestamp |
| `is_superuser` | BooleanField | Django superuser flag |
| `username` | CharField | Unique username |
| `first_name` | CharField | User's first name |
| `last_name` | CharField | User's last name |
| `email` | CharField | Email address |
| `is_staff` | BooleanField | Staff access flag |
| `is_active` | BooleanField | Account active status |
| `date_joined` | DateTimeField | Registration date |
| `phone_number` | CharField | Contact number |
| `user_type` | CharField | 'normal' or 'admin' |
| `account_status` | CharField | 'active' or 'suspended' |
| `suspension_reason` | TextField | Reason for suspension |
| `suspended_by` | ForeignKey | Admin who suspended |
| `suspension_date` | DateTimeField | When suspended |
| `last_login_attempt` | DateTimeField | Last login try |

**Current Records**: 10 users
- 9 Normal users
- 1 Admin user

---

### 2. **items_item** (Lost & Found Items)
**Purpose**: Stores all reported lost and found items

| Field Name | Type | Description |
|------------|------|-------------|
| `id` | BigAutoField | Primary key |
| `user` | ForeignKey | User who reported item |
| `title` | CharField | Item title/name |
| `description` | TextField | Detailed description |
| `category` | CharField | electronics, accessories, etc. |
| `status` | CharField | 'LOST' or 'FOUND' |
| `location` | CharField | Where item was lost/found |
| `image` | FileField | Photo of the item |
| `created_at` | DateTimeField | Report timestamp |

**Current Records**: 12 items
- Lost items: ~6
- Found items: ~6

**Categories Available**:
- Electronics (phones, chargers, etc.)
- Accessories (bags, keys, etc.)
- Documents
- Clothing
- Other

---

### 3. **items_claim** (Ownership Claims)
**Purpose**: Tracks claims submitted by users for items

| Field Name | Type | Description |
|------------|------|-------------|
| `id` | BigAutoField | Primary key |
| `item` | ForeignKey | Item being claimed |
| `claimant` | ForeignKey | User making claim |
| `claim_type` | CharField | 'ownership' or 'found_my_item' |
| `proof_description` | TextField | Evidence of ownership |
| `status` | CharField | PENDING, APPROVED, REJECTED |
| `verified_by` | ForeignKey | Admin who verified |
| `verification_date` | DateTimeField | When verified |
| `verification_notes` | TextField | Admin's notes |
| `created_at` | DateTimeField | Claim submission time |

**Current Records**: 18 claims

**Claim Types**:
1. **Ownership Claims**: User claims someone else's found item
2. **Found My Item**: User found their own lost item

**Claim Statuses**:
- `PENDING`: Awaiting admin review
- `UNDER_REVIEW`: Admin is reviewing
- `APPROVED`: Claim verified and approved
- `REJECTED`: Claim denied

---

### 4. **items_message** (Messaging System)
**Purpose**: Stores all messages between users

| Field Name | Type | Description |
|------------|------|-------------|
| `id` | BigAutoField | Primary key |
| `sender` | ForeignKey | User sending message |
| `receiver` | ForeignKey | User receiving message |
| `content` | TextField | Message text |
| `timestamp` | DateTimeField | When message was sent |

**Current Records**: 36 messages
- Active conversations between multiple users
- Two-way communication enabled

---

## 🔗 Relationships

### User → Items (One-to-Many)
- One user can report multiple items
- Each item belongs to one user

### User → Claims (One-to-Many)
- One user can submit multiple claims
- Each claim belongs to one user (claimant)

### Item → Claims (One-to-Many)
- One item can have multiple claims
- Each claim is for one specific item

### User → Messages (Many-to-Many via sender/receiver)
- Users can send messages to multiple users
- Users can receive messages from multiple users
- Creates conversation threads

### Admin → User Suspension (One-to-Many)
- One admin can suspend multiple users
- Each suspension is performed by one admin

### Admin → Claim Verification (One-to-Many)
- One admin can verify multiple claims
- Each claim is verified by one admin

---

## 📈 Database Statistics

| Table | Records | Purpose |
|-------|---------|---------|
| **accounts_customuser** | 10 | User accounts |
| **items_item** | 12 | Lost/Found items |
| **items_claim** | 18 | Ownership claims |
| **items_message** | 36 | User messages |
| **TOTAL** | **76** | All records |

---

## 🔐 Security Features

1. **Password Hashing**: All passwords stored with Django's secure hashing
2. **Foreign Key Constraints**: Maintains data integrity
3. **User Type Validation**: Separates normal users from admins
4. **Account Status**: Can suspend problematic accounts
5. **Claim Verification**: Admin approval required for claims

---

## 🎯 Key Features Enabled by Schema

### For Users:
- ✅ Report lost/found items with photos
- ✅ Submit ownership claims with proof
- ✅ Message other users securely
- ✅ Track claim history
- ✅ Update profile information

### For Admins:
- ✅ Verify and approve claims
- ✅ Suspend/reactivate user accounts
- ✅ View all system activity
- ✅ Manage user disputes
- ✅ Track verification history

---

## 💡 Potential Enhancements

### Suggested Additional Tables:
1. **Notifications**: Alert users about claim updates
2. **Item Categories**: More detailed categorization
3. **User Ratings**: Rate successful exchanges
4. **Activity Log**: Track all system actions
5. **Reports**: Flag inappropriate content

### Suggested Fields to Add:
1. **Item.reward_offered**: Optional reward amount
2. **Item.expiry_date**: Auto-archive old items
3. **Message.read_status**: Track read/unread
4. **User.reputation_score**: Trust rating
5. **Claim.priority**: Urgent vs normal claims