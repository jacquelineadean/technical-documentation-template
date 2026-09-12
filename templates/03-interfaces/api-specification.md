---
doc_id: API-<SCOPE>-001
title: <API Name> — API Specification
doc_type: api
status: draft
version: 0.1.0
owner: <Integration Lead role>
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
tags: [api, interface]
---

# \<API Name\> — API Specification

> **Purpose.** Synchronous request/response interfaces. Complements a machine-readable
> schema (OpenAPI, WSDL, protobuf) rather than replacing it: the schema defines the shape,
> this defines the **behaviour and the semantics** — idempotency, ordering, consistency,
> error meaning, and what a caller should do about each.
>
> Keep the schema authoritative for field-level structure and link to it. Duplicating a
> schema in prose guarantees the two diverge.

---

## 1. Overview

| | |
| --- | --- |
| API name | |
| Interface ID | IF-… |
| API version | |
| Style | REST / SOAP / gRPC / GraphQL |
| Machine-readable spec | *(link)* |
| Base URL (logical) | |
| Owner | |
| Consumers | |
| Criticality | |
| Status | Draft / Live / Deprecated |

---

## 2. Authentication and authorisation

| | |
| --- | --- |
| Authentication | |
| Credential type | |
| Credential issuance | |
| Rotation | |
| Token lifetime | |
| Authorisation model | |
| Scopes / permissions | |
| Data-level restrictions | *(e.g. a partner may only see their own orders — state where this is enforced)* |

| Scope | Grants | Granted to |
| --- | --- | --- |
| | | |

---

## 3. Conventions

| Aspect | Convention |
| --- | --- |
| Content type | |
| Character encoding | |
| Date/time format | ISO-8601 with offset |
| Timezone | |
| Decimal representation | *(string for monetary values to avoid float representation error)* |
| Null vs. absent | |
| Field naming | |
| Enumerations | *(closed set — consumers must tolerate new values, or open set)* |
| Correlation ID header | |
| Request ID / idempotency header | |
| API version signalling | *(path, header, media type)* |

---

## 4. Operations

### 4.1 `<METHOD> /<path>`

| | |
| --- | --- |
| Purpose | |
| Idempotent | |
| Safe | |
| Authorisation | |
| Rate limit | |
| Timeout (server) | |
| Recommended client timeout | |

**Request**

| Parameter | In | Type | Required | Description | Example |
| --- | --- | --- | --- | --- | --- |
| | path / query / header / body | | | | |

```json
{ }
```

**Response — success**

| Status | Meaning | Body |
| --- | --- | --- |
| 200 | | |
| 201 | | |
| 202 | *(accepted for async processing — state how the caller learns the outcome)* | |

```json
{ }
```

**Response — errors**

| Status | Code | Meaning | Caller action | Retryable |
| --- | --- | --- | --- | --- |
| 400 | | | | No |
| 401 | | | | No |
| 403 | | | | No |
| 404 | | | | No |
| 409 | | | | Depends |
| 422 | | | | No |
| 429 | | | Back off per `Retry-After` | Yes |
| 500 | | | | Yes |
| 503 | | | | Yes |

**Semantics**

| Aspect | Behaviour |
| --- | --- |
| Consistency | *(read-after-write? eventual? state the window)* |
| Side effects | |
| Partial success | *(possible? how represented?)* |
| Concurrency control | *(ETag / version field / last-write-wins)* |

---

## 5. Idempotency

| | |
| --- | --- |
| Idempotency mechanism | |
| Key source | |
| Key scope | |
| Retention window | |
| Behaviour on replay | *(replays the original response, or re-executes?)* |
| Behaviour on key reuse with a different body | |

> Any operation that creates a resource or moves money needs an idempotency key, because a
> client that times out cannot know whether the request was applied. Without one, the
> client's only safe choices are to retry and risk duplication, or not retry and risk loss.

---

## 6. Pagination, filtering, sorting

| Aspect | Approach |
| --- | --- |
| Pagination style | Offset / Cursor |
| Page size default / max | |
| Stability under concurrent modification | *(offset pagination skips or repeats rows when the underlying set changes)* |
| Total count provided | |
| Filtering | |
| Sorting | |
| Default ordering | |

---

## 7. Rate limiting

| Consumer class | Limit | Window | Burst | On exceed | Headers |
| --- | --- | --- | --- | --- | --- |
| | | | | 429 + `Retry-After` | |

---

## 8. Performance

| Operation | p50 | p95 | p99 | Timeout | Max payload |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

| Consumer | Expected RPS | Peak RPS | Peak driver |
| --- | --- | --- | --- | 
| | | | |

---

## 9. Asynchronous patterns

> For operations returning `202`.

| Aspect | Detail |
| --- | --- |
| Acceptance response | |
| Status polling endpoint | |
| Callback / webhook | |
| Callback authentication | |
| Callback retry policy | |
| Terminal states | |
| Maximum processing time | |
| Behaviour if the caller never polls | |

---

## 10. Versioning and deprecation

| Aspect | Policy |
| --- | --- |
| Versioning scheme | |
| Breaking change definition | |
| Supported versions | |
| Deprecation notice | |
| Sunset headers | |
| Migration support | |

---

## 11. Observability

| Signal | Detail |
| --- | --- |
| Correlation ID propagation | |
| Request logging | |
| Sensitive fields excluded from logs | |
| Metrics exposed | |
| Health endpoint | |
| Status page | |

---

## 12. Client guidance

| Guidance | Detail |
| --- | --- |
| Recommended timeout | |
| Retry policy | *(which statuses, how many attempts, what backoff, with jitter)* |
| Circuit breaker | |
| Caching | |
| Connection pooling | |
| Behaviour when the API is unavailable | |

---

## 13. Testing

| Environment | Base URL | Credentials | Data | Rate limits |
| --- | --- | --- | --- | --- |
| Sandbox | | | | |

| Test | Scenario | Expected |
| --- | --- | --- |
| | | |

---

## Change log

| Version | Date | Author | Change | Breaking |
| --- | --- | --- | --- | --- |
| 0.1.0 | | | Initial draft | — |
