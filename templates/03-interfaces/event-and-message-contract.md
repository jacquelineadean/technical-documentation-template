---
doc_id: EMC-<SCOPE>-001
title: <Event or Message Name> — Event and Message Contract
doc_type: emc
status: draft
version: 0.1.0
owner: <Producing team role>
created: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
next_review: <YYYY-MM-DD>
review_cycle: semi-annual
classification: internal
systems: [<SYSTEM_CODE>]
domains: []
upstream_docs: [ICAT-<SCOPE>-001]
downstream_docs: []
related_interfaces: []
tags: [event, message, async]
---

# \<Event or Message Name\> — Event and Message Contract

> **Purpose.** Asynchronous interfaces: schema, keys, ordering, delivery semantics, and
> replay. The properties that matter in async integration are exactly the ones that are
> invisible in the payload, so they are stated explicitly here.

---

## 1. Identification

| | |
| --- | --- |
| Name | |
| Interface ID | IF-… |
| Schema version | |
| Kind | Event *(something happened)* / Command *(do something)* / Document *(here is state)* |
| Producer | |
| Consumers | |
| Destination | *(topic / queue / exchange)* |
| Criticality | |

**Kind matters.** An *event* is a statement of fact the producer does not care who consumes;
a *command* is directed at one consumer and expects execution. Publishing a command as an
event, or vice versa, produces coupling that is hard to unpick later.

---

## 2. Trigger

| | |
| --- | --- |
| Published when | |
| Published by | |
| Timing relative to the state change | *(before commit / after commit / eventually)* |
| Guaranteed published | *(is publication transactional with the state change? If not, the event can be lost or emitted without the change)* |
| Frequency | |
| Volume — typical / peak | |
| Peak driver | |

> "Guaranteed published" is the question that determines whether consumers can trust the
> stream as a complete record. Without transactional publication (outbox pattern or
> equivalent), consumers must reconcile against the source periodically — and that
> obligation belongs in this document, not in each consumer's assumptions.

---

## 3. Schema

| | |
| --- | --- |
| Format | JSON / Avro / Protobuf / XML |
| Schema registry | |
| Schema ID | |
| Compatibility mode | Backward / Forward / Full / None |

**Envelope**

| Field | Type | Req | Description |
| --- | --- | --- | --- |
| `eventId` | uuid | M | Unique per event instance |
| `eventType` | string | M | |
| `eventVersion` | string | M | |
| `occurredAt` | timestamp | M | When the fact happened, in the source's clock |
| `publishedAt` | timestamp | M | When it was emitted |
| `producer` | string | M | |
| `correlationId` | string | M | Traces a business transaction across services |
| `causationId` | string | O | The event that caused this one |
| `partitionKey` | string | M | Determines ordering scope |
| `payload` | object | M | |

> `occurredAt` and `publishedAt` differ whenever publication is delayed or replayed, and
> consumers doing time-window aggregation need to know which one to use. State it.

**Payload**

| Field | Type | Req | Description | Valid values | Example |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Example**

```json
{ }
```

**Payload style**

| Style | Used | Rationale |
| --- | --- | --- |
| Thin — identifiers only, consumer fetches | | Small, but couples consumers to the producer's API and its availability |
| Fat — full state | | Self-contained, but larger and can become stale on replay |
| Delta — what changed | | Compact, but requires consumers to hold prior state |

---

## 4. Keys and ordering

| | |
| --- | --- |
| Partition key | |
| Ordering guarantee | Global / Per key / None |
| Ordering scope | |
| Sequence number | |
| Gap detection | |
| Out-of-order handling | |

> Ordering is almost always *per key*, not global. Consumers relying on global ordering are
> relying on an accident of current volume, and will break under load.

---

## 5. Delivery semantics

| | |
| --- | --- |
| Guarantee | At-most-once / At-least-once |
| Duplicates possible | |
| Idempotency key | |
| Consumer de-duplication requirement | |
| De-duplication window | |
| Redelivery on failure | |
| Maximum redeliveries | |
| Dead-letter destination | |
| Poison message handling | |

**Consumer obligation:** with at-least-once delivery, consumers **must** be idempotent.
State the key and the window here so every consumer implements the same de-duplication.

---

## 6. Retention and replay

| | |
| --- | --- |
| Retention | |
| Replay supported | |
| Replay mechanism | |
| Replay authorisation | |
| Replay side effects | *(will consumers re-execute? which are safe?)* |
| Compaction | |
| Consumer offset handling | |

**Replay safety by consumer**

| Consumer | Idempotent | Safe to replay | Constraints |
| --- | --- | --- | --- |
| | | | |

> Replay is the recovery mechanism for async systems, and it is unusable if any consumer
> re-executes a side effect. Establish this per consumer *before* you need to replay.

---

## 7. Consumers

| Consumer | Purpose | Fields used | Criticality | Lag tolerance | Contact |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

**Consumer obligations**

| Obligation | Detail |
| --- | --- |
| Tolerate unknown fields | Required — producers add optional fields without notice |
| Tolerate unknown enum values | State the required behaviour |
| Idempotent processing | Required |
| Consume within | |
| Report failures | |
| Test against new schema versions within | |

---

## 8. Error handling

| Failure | Producer behaviour | Consumer behaviour | Detection |
| --- | --- | --- | --- |
| Broker unavailable at publish | | — | |
| Schema validation failure | | | |
| Consumer processing failure — transient | — | | |
| Consumer processing failure — permanent | — | | |
| Poison message | — | | |
| Consumer lag exceeds threshold | | | |

---

## 9. Monitoring

| Signal | Threshold | Owner | Alert |
| --- | --- | --- | --- |
| Publish rate | | | |
| Publish failures | | | |
| Consumer lag | | | |
| Dead-letter arrivals | | | |
| Processing errors | | | |
| End-to-end latency | | | |
| **No events published within expected interval** | | | |

---

## 10. Versioning

| Aspect | Policy |
| --- | --- |
| Versioning scheme | |
| Compatibility mode | |
| Breaking change definition | |
| Notice period | |
| Parallel version support | |
| Deprecation | |

| Change | Breaking under backward compatibility |
| --- | --- |
| Add optional field | No |
| Add required field | Yes |
| Remove field | Yes |
| Change type | Yes |
| Add enum value | Yes if consumers switch exhaustively |
| Change semantic meaning | **Yes** — and undetectable by schema checks |
| Change partition key | **Yes** — changes ordering guarantees |

---

## Change log

| Version | Date | Author | Change | Breaking |
| --- | --- | --- | --- | --- |
| 0.1.0 | | | Initial draft | — |
