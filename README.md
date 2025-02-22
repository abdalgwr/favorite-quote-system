# Favorite Quotes Microservice

## Overview
This microservice provides a **ZeroMQ-based API** for managing favorite quotes. Users can:
- **Save a quote** to favorites.
- **Retrieve a list of favorite quotes**.
- **Remove a quote from favorites**.

This microservice communicates using **ZeroMQ REQ-REP pattern**, meaning each request **expects** a corresponding response.

---

## **Communication Contract**
See below

### **How to REQUEST Data from the Microservice**
All communication is done using **ZeroMQ**. To send a request, create a ZeroMQ `REQ` socket and send one of the following commands.

#### **1. Save a Quote**
**Request format:**
