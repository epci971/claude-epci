# Guarantee Rules — Security Deposit Calculation

## Auto-Calculation Formula

```
rate = 0.30           // 30% of net total
raw = totalNet × rate
rounded = ceil(raw / 50) × 50   // round up to nearest 50€
deposit = max(300, min(1500, rounded))  // clamp between floor and cap
```

## Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Rate | 30% | Industry standard for seasonal rental (20-30% recommended) |
| Floor | 300 € | Minimum dissuasive amount even for small stays |
| Cap | 1500 € | Avoids psychologically prohibitive amounts |
| Rounding | Nearest 50€ up | Clean professional amounts |

## Examples

| Scenario | Net Total | 30% | Rounded | Clamped | Final |
|----------|-----------|-----|---------|---------|-------|
| Ti Briz 1 week low season | 600 € | 180 | 200 | 300 (floor) | **300 €** |
| Kaz Alizé 1 week | 1100 € | 330 | 350 | 350 | **350 €** |
| 3 accommodations (Dupuy) | 2320 € | 696 | 700 | 700 | **700 €** |
| High season 3 accommodations | 4000 € | 1200 | 1200 | 1200 | **1200 €** |
| Exceptional booking | 6000 € | 1800 | 1800 | 1500 (cap) | **1500 €** |

## Override

The owner can override the auto-calculated amount when:
- Client brings pets (higher risk)
- Special event booking (party, wedding)
- Client with specific equipment needs

Use flag: `--override-garantie {amount}`

## Deposit Options (client's choice)

### Option A: Cheque
- Made out to: Edouard PHELIP
- Given at check-in
- Not cashed unless damage is found
- Returned or destroyed after état des lieux de sortie

### Option B: Swikly (secure bank imprint)
- Link sent to client before stay via email
- No amount debited unless damage is found
- Imprint released within 7 days of departure
- Website: www.swikly.com

## Legal Context

- No legal cap on security deposit for seasonal rental in France
- Best practice: 20-30% of stay total, never exceeding total rent
- If damage exceeds deposit: owner can claim the balance (amicable, then legal recourse)
- Justification required: itemized quotes or invoices for any withholding
- Owner's insurance (PNO) provides additional coverage
- Tenant's RC/villégiature insurance is the primary recourse for major damage
