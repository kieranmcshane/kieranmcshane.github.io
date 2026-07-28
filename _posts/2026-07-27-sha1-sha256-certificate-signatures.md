---
layout: post
math: true
title: "From SHA-1 to SHA-256 in a Certificate Signature"
subtitle: "Collision resistance, birthday bounds, and what is actually being signed"
date: 2026-07-27 09:00:00 +0200
categories: [cryptography]
tags: [SHA-1, SHA-256, digital-signatures, certificates, collision-resistance]
excerpt: "Why replacing SHA-1 by SHA-256 in a certificate matters, how the birthday bound enters, and why a hash function is only one component of a digital signature."
---

I recently inspected the self-signed certificate of an old network printer. One line read

```text
Signature Algorithm: sha1WithRSAEncryption
```

After the certificate was regenerated, the corresponding line read

```text
Signature Algorithm: sha256WithRSAEncryption
```

The change looks small, but it joins several different pieces of mathematics. <span id="definition-sha" class="definition-target">SHA means **Secure Hash Algorithm**; SHA-1 and SHA-256 are standardized hash functions</span>. <span id="definition-rsa" class="definition-target">RSA—named after Ron Rivest, Adi Shamir and Leonard Adleman—is a public-key primitive: the private key performs the signing operation, while the related public key lets anyone verify it</span>. <span id="definition-x509" class="definition-target">X.509 is the international standard that specifies the structure of a public-key certificate</span>. It is worth separating those roles before asking why SHA-256 is the better choice.

The printer also supplied a useful cautionary example. Its secure web service had stopped responding and came back after a restart; the old certificate itself had not expired. Replacing SHA-1 was still sensible, but it was not the explanation for every connection problem.

Technical vocabulary is expanded where it first matters. On later occurrences, a dotted term can be hovered or focused for a short definition and followed to return to the fuller explanation.

## Hashing is not signing

SHA-256 is a hash function, not a signature algorithm. It becomes part of a signature only when a signature scheme such as <a class="concept-ref" href="#definition-rsa" data-definition="RSA: the Rivest–Shamir–Adleman public-key primitive used here for digital signatures.">RSA</a> signs an encoding of its output.

A fixed-output hash function is a map

$$
H:\{0,1\}^{*}\longrightarrow\{0,1\}^{n}.
$$

It accepts a bit string of arbitrary finite length and returns an <span id="definition-digest" class="definition-target">$n$-bit **digest**, the fixed-length output used as a compact fingerprint of the input</span>. SHA-1 has $n=160$; <a class="concept-ref" href="#definition-sha" data-definition="SHA: Secure Hash Algorithm, the standardized family containing SHA-1 and SHA-2.">SHA-256</a> has $n=256$. Both are specified by the <span id="definition-nist" class="definition-target">US **National Institute of Standards and Technology** (NIST)</span> in its Secure Hash Standard, [Federal Information Processing Standard 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) (FIPS 180-4). SHA-256 belongs to the SHA-2 family and is not simply “SHA-1 with a longer output.”

A hash function has no secret key. Anyone can compute $H(M)$, so a digest alone cannot identify the author of a message. A <span id="definition-digital-signature" class="definition-target">**digital signature** uses a private signing key to authenticate a message and detect changes; it does not ordinarily hide the message</span>:

$$
\sigma=\operatorname{Sign}_{sk}\!\bigl(H(M)\bigr).
$$

The verifier recomputes $H(M)$ and checks $\sigma$ with the public key $pk$. Actual schemes specify an encoding around the digest and may use randomness, but the division of labour remains:

- the hash function reduces the message to a fixed-size value;
- the signature scheme binds that value to a private key;
- the certificate binds a public key to a stated subject.

<a class="concept-ref" href="#definition-nist" data-definition="NIST: the US National Institute of Standards and Technology, which publishes the FIPS cryptographic standards cited here.">NIST</a> therefore standardizes hash functions in [FIPS 180-4](https://doi.org/10.6028/NIST.FIPS.180-4) and signature schemes in the separate Digital Signature Standard, [FIPS 186-5](https://csrc.nist.gov/pubs/fips/186-5/final). <span id="definition-fips" class="definition-target">**FIPS** means **Federal Information Processing Standard**, a US federal technical standard published here by NIST</span>.

## Three inverse problems

The security of an ideal $n$-bit hash is usually organized around three search problems. <span id="definition-hash-search-problems" class="definition-target">A **preimage** attack starts from a target digest and seeks an input; a **second-preimage** attack starts from one input and seeks a different input with the same digest; a **collision** attack may choose both distinct inputs</span>.

| Property | The adversary is asked to find | Generic work for an ideal $n$-bit hash |
|---|---|---:|
| Preimage resistance | given $y$, an $M$ such that $H(M)=y$ | about $2^n$ |
| Second-preimage resistance | given $M$, a different $M'$ with $H(M')=H(M)$ | about $2^n$ |
| Collision resistance | any distinct $M,M'$ with $H(M)=H(M')$ | about $2^{n/2}$ |

The last exponent is smaller because the attacker may choose both messages. This is the birthday phenomenon.

Suppose that $H$ behaves like a uniformly random map into a set of size $N=2^n$. After evaluating $q$ distinct inputs, the probability of seeing no collision is

$$
\Pr(\text{no collision})
=
\prod_{j=0}^{q-1}\left(1-\frac{j}{N}\right).
$$

When $q$ is much smaller than $N$, use $\log(1-x)\approx-x$:

$$
\log\Pr(\text{no collision})
\approx
-\sum_{j=0}^{q-1}\frac{j}{N}
=
-\frac{q(q-1)}{2N}.
$$

Thus

$$
\Pr(\text{at least one collision})
\approx
1-\exp\!\left(-\frac{q(q-1)}{2^{n+1}}\right).
$$

Setting this probability equal to $1/2$ gives

$$
q_{1/2}
\approx
\sqrt{2\log 2}\,2^{n/2}
\approx
1.1774\,2^{n/2}.
$$

The digest length therefore suggests $80$ bits of generic collision resistance for SHA-1 and $128$ bits for SHA-256. These numbers describe an idealized random function. A concrete hash algorithm can be weaker if its internal structure supplies a shortcut.

### What the number 256 actually controls

The number in “SHA-256” is the digest length:

$$
256\ \text{bits}
=
32\ \text{bytes}
=
64\ \text{hexadecimal digits}.
$$

The last equality holds because one hexadecimal digit encodes four bits. It is convenient, but it is not a security theorem. The security estimates come from the search problem:

| Task against an ideal SHA-256-like function | Generic classical scale |
|---|---:|
| Find a preimage of a prescribed digest | $2^{256}$ |
| Find any collision | $2^{128}$ |
| Guess a uniformly random 256-bit value | probability $2^{-256}$ per attempt |

The distinction explains why “256-bit hash” should not automatically be read as “256 bits of security.” NIST’s security-strength table assigns SHA-256 a collision strength of $128$ bits and a preimage strength of $256$ bits under its stated model.

<figure class="source-facsimile source-facsimile--wide">
  <div class="source-facsimile-viewport">
    <a class="source-facsimile-link" href="https://csrc.nist.gov/Projects/hash-functions#security-strengths-of-approved-hash-functions" target="_blank" rel="noopener" aria-label="Open NIST’s complete security-strength table">
      <img src="{{ '/assets/images/source-excerpts/sha256-nist-security-strengths.png' | relative_url }}" alt="Facsimile of NIST’s security-strength table. The highlighted SHA-256 row gives 128 bits for collision resistance and 256 bits for preimage resistance." loading="lazy" decoding="async">
    </a>
  </div>
  <figcaption><strong>Source excerpt.</strong> NIST’s table separates the two figures: the highlighted SHA-256 row gives 128-bit collision strength and 256-bit preimage strength. Yellow highlighting added. <a href="https://csrc.nist.gov/Projects/hash-functions#security-strengths-of-approved-hash-functions" target="_blank" rel="noopener">Open the complete table ↗</a></figcaption>
</figure>

## The iterated structure

SHA-1 and SHA-256 both pad the message, divide it into $512$-bit blocks, and update a fixed-size state. In schematic form,

$$
h_0=\mathrm{IV},
\qquad
h_i=C(h_{i-1},M_i),
\qquad
H(M)=h_\ell.
$$

Here <span id="definition-iv" class="definition-target">$\mathrm{IV}$ is the public **initialization vector**, the fixed state from which every hash computation begins</span>. <span id="definition-compression-function" class="definition-target">$C$ is a **compression function**: it combines one fixed-size message block with the current fixed-size internal state to produce the next state</span>. The values $h_i$ are called <span id="definition-chaining-state" class="definition-target">**chaining states** because each block inherits the state produced by the preceding block</span>, and $M_1,\ldots,M_\ell$ are the padded blocks. This repeated construction is the <span id="definition-merkle-damgard" class="definition-target">**Merkle–Damgård pattern**: pad the message, process its blocks sequentially through one compression function, and publish the final chaining state</span>. The padding records the message length, so two different parses cannot be confused merely by appending zeros.

SHA-256 stores eight $32$-bit state words. During each of its $64$ steps it computes, modulo $2^{32}$,

$$
T_1
=
h+\Sigma_1(e)+\operatorname{Ch}(e,f,g)+K_t+W_t,
$$

$$
T_2
=
\Sigma_0(a)+\operatorname{Maj}(a,b,c),
$$

where

$$
\operatorname{Ch}(x,y,z)
=(x\wedge y)\oplus(\neg x\wedge z),
$$

$$
\operatorname{Maj}(x,y,z)
=(x\wedge y)\oplus(x\wedge z)\oplus(y\wedge z),
$$

and $\Sigma_0,\Sigma_1$ combine rotations of a $32$-bit word. The Boolean functions are defined in [Section 4.1.2 of FIPS 180-4](https://csrc.nist.gov/files/pubs/fips/180-4/final/docs/fips180-4.pdf#page=14), while the complete SHA-256 round update appears in [Section 6.2](https://csrc.nist.gov/files/pubs/fips/180-4/final/docs/fips180-4.pdf#page=26).

The purpose of these operations is diffusion: a small input difference should spread through the state in a way that is hard to control. Collision cryptanalysis looks for the opposite—a carefully chosen difference whose propagation can be predicted and eventually cancelled.

### The equations in 32-bit C

The round equations translate closely into unsigned 32-bit arithmetic. For example:

```c
#include <stdint.h>

static inline uint32_t rotr32(uint32_t x, unsigned n) {
    /* SHA-256 calls this only with 1 <= n < 32. */
    return (x >> n) | (x << (32u - n));
}

static inline uint32_t choose(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (~x & z);
}

static inline uint32_t majority(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (x & z) ^ (y & z);
}

static inline uint32_t big_sigma_1(uint32_t x) {
    return rotr32(x, 6) ^ rotr32(x, 11) ^ rotr32(x, 25);
}
```

The C type `uint32_t` is an unsigned integer represented by exactly $32$ bits. It matters because unsigned overflow implements addition modulo $2^{32}$, exactly as required by the standard. A complete implementation still has to get <span id="definition-byte-order" class="definition-target">**byte order**, the convention for arranging the bytes of a multi-byte word</span>; padding; <span id="definition-message-schedule" class="definition-target">the **message schedule**, which expands the input block into the words consumed by the rounds</span>; all $64$ constants; state updates; and arbitrarily long inputs right. The fragment above explains the correspondence with the formulas; it is not a substitute for a reviewed cryptographic library.

A useful end-to-end check is the official [NIST one-block example](https://csrc.nist.gov/csrc/media/projects/cryptographic-standards-and-guidelines/documents/examples/sha256.pdf). It gives

```text
SHA-256("abc")
= ba7816bf8f01cfea414140de5dae2223
  b00361a396177a9cb410ff61f20015ad
```

Here the three ASCII bytes are followed by the mandatory padding and processed as one $512$-bit block. Reproducing the digest is a necessary implementation check, not evidence that an implementation is secure against <span id="definition-side-channel" class="definition-target">**side channels**, which leak secrets through timing, power use, cache behaviour or another physical effect outside the intended mathematical input and output</span>, or malformed inputs.

### Length extension and why HMAC has two layers

<a class="concept-ref" href="#definition-merkle-damgard" data-definition="Merkle–Damgård: an iterated hash construction that chains one compression function across padded message blocks.">Merkle–Damgård</a> iteration has a consequence that is separate from collisions. Given $H(M)$ and the length of $M$, an attacker can use the published <a class="concept-ref" href="#definition-digest" data-definition="Digest: the fixed-length output of a hash function.">digest</a> as a new <a class="concept-ref" href="#definition-chaining-state" data-definition="Chaining state: the fixed-size internal value passed from one hash block to the next.">chaining state</a> and compute

$$
H\!\left(M\,\|\,\operatorname{pad}(M)\,\|\,X\right)
$$

for a chosen suffix $X$, without knowing $M$. This is a <span id="definition-length-extension" class="definition-target">**length-extension attack**: the attacker continues the public chaining state to hash an added suffix without recovering the original message</span>. It does not invert the hash and does not produce two equal digests. It shows instead why the naive construction

$$
\operatorname{MAC}_K(M)=H(K\|M)
$$

is not a safe general-purpose <span id="definition-mac" class="definition-target">**message-authentication code** (MAC), a keyed tag used to check both message integrity and possession of a shared secret key</span>, when instantiated directly with SHA-256.

<span id="definition-hmac" class="definition-target">**HMAC** means **Hash-based Message Authentication Code**</span>. It changes the construction:

$$
\operatorname{HMAC}_K(M)
=
H\!\left((K'\oplus\mathrm{opad})
\,\|\,
H((K'\oplus\mathrm{ipad})\|M)\right).
$$

The inner digest is therefore not exposed as the final state of a message that an attacker can simply continue. The precise definition, including the fixed `ipad` and `opad` blocks, appears in [Section 2 of RFC 2104](https://www.rfc-editor.org/rfc/rfc2104.html#section-2). <span id="definition-rfc" class="definition-target">An **RFC**, or **Request for Comments**, is a numbered technical publication in the Internet standards series</span>. This is another reason that “use SHA-256” is incomplete advice: the surrounding construction determines what security property is obtained.

## What failed in SHA-1

SHA-1’s $160$-bit output would suggest a generic collision cost around $2^{80}$. Its round structure permits substantially better <span id="definition-differential-attack" class="definition-target">**differential attacks**, which engineer and track carefully chosen input differences through the internal rounds instead of treating the hash as a black box</span>. In 2017, Marc Stevens, Elie Bursztein, Pierre Karpman, Ange Albertini and Yarik Markov produced two different PDF files with exactly the same SHA-1 digest. Their SHAttered paper estimates the computation at roughly $2^{63.1}$ SHA-1 compressions.

<figure class="source-facsimile source-facsimile--paper">
  <div class="source-facsimile-viewport">
    <a class="source-facsimile-link" href="https://shattered.io/static/shattered.pdf#page=2" target="_blank" rel="noopener" aria-label="Open the complete SHAttered paper">
      <img src="{{ '/assets/images/source-excerpts/sha1-shattered-abstract.png' | relative_url }}" alt="Facsimile of the SHAttered paper’s title and abstract. Highlighted passages announce the first practical collision for full SHA-1 and estimate its cost at 2 to the power 63.1 SHA-1 compressions." loading="lazy" decoding="async">
    </a>
  </div>
  <figcaption><strong>Source excerpt.</strong> The abstract of Stevens and coauthors reports the first practical collision for full SHA-1 and estimates a cost of about $2^{63.1}$ compression calls. This is a collision result, not a preimage attack or key recovery. Yellow highlighting added. <a href="https://shattered.io/static/shattered.pdf#page=2" target="_blank" rel="noopener">Open the complete paper ↗</a></figcaption>
</figure>

That result did not produce arbitrary <a class="concept-ref" href="#definition-hash-search-problems" data-definition="Preimage attack: given a target digest, find an input that hashes to it.">preimages</a>, reveal private RSA keys or invert SHA-1 in general. It did something narrower and decisive: it exhibited a practical <a class="concept-ref" href="#definition-hash-search-problems" data-definition="Collision attack: find any two distinct inputs with the same digest.">collision</a> for the full hash function. Collision resistance is precisely the property needed to prevent one signature from being transferred between two messages with the same digest.

NIST had already discouraged SHA-1 for signature generation before the public collision. It now plans to [remove SHA-1 from all remaining applications by the end of 2030](https://csrc.nist.gov/News/2022/nist-transitioning-away-from-sha-1-for-all-apps). SHA-256 remains an approved member of <a class="concept-ref" href="#definition-sha2" data-definition="SHA-2: the standardized hash family containing SHA-224, SHA-256, SHA-384 and SHA-512 variants.">SHA-2</a>. No accepted practical collision attack is known for the full $64$-step SHA-256 function; published attacks concern reduced or otherwise modified versions.

## How a collision crosses into RSA

For a concrete model, consider `RSASSA-PKCS1-v1_5`: **RSASSA** means **RSA Signature Scheme with Appendix**, and “with appendix” means that verification requires the original message as well as the signature. This deterministic scheme uses the version 1.5 encoding specified by <span id="definition-pkcs1" class="definition-target">**PKCS #1**, the RSA specification in the **Public-Key Cryptography Standards** series</span>. Let

$$
N=pq,
\qquad
ed\equiv1\pmod{\lambda(N)}.
$$

Here $N$ is the <span id="definition-rsa-modulus" class="definition-target">**RSA modulus**, the product of two secret primes</span>. The private exponent is $d$ and the public exponent is $e$; their congruence makes the two modular exponentiations inverse operations on the required inputs. The standard does not exponentiate the raw hash. It first builds a precisely formatted encoded message

$$
\operatorname{EM}=\operatorname{EMSA}_{H}(M),
$$

where **EM** means “encoded message” and **EMSA** means “Encoding Method for Signatures with Appendix.” It contains padding and an <span id="definition-asn1" class="definition-target">**ASN.1** `DigestInfo` value. **Abstract Syntax Notation One** is a language for describing typed data structures independently of their concrete byte encoding</span>; here the structure identifies $H$. The signature is

$$
s\equiv \operatorname{EM}^{\,d}\pmod N,
$$

and verification checks that

$$
s^e\equiv \operatorname{EMSA}_{H}(M)\pmod N.
$$

The exact signature procedure is given by <a class="concept-ref" href="#definition-pkcs1" data-definition="PKCS #1: the RSA specification in the Public-Key Cryptography Standards series.">PKCS #1</a> in [Section 8.2](https://www.rfc-editor.org/rfc/rfc8017.html#section-8.2); its message encoding is specified separately in Section 9.2.

<figure class="source-facsimile source-facsimile--wide">
  <div class="source-facsimile-viewport">
    <a class="source-facsimile-link" href="https://www.rfc-editor.org/rfc/rfc8017.html#section-9.2" target="_blank" rel="noopener" aria-label="Open RFC 8017 Section 9.2">
      <img src="{{ '/assets/images/source-excerpts/sha256-rfc8017-encoding.png' | relative_url }}" alt="Facsimile of RFC 8017 Section 9.2. The highlighted lines name digestAlgorithm inside DigestInfo and show the padded encoded message EM." loading="lazy" decoding="async">
    </a>
  </div>
  <figcaption><strong>Source excerpt.</strong> RFC 8017 names the hash algorithm inside <code>DigestInfo</code>, then places that structure inside the padded encoded message <code>EM</code>. RSA therefore signs neither the original message nor a bare hash. Yellow highlighting added. <a href="https://www.rfc-editor.org/rfc/rfc8017.html#section-9.2" target="_blank" rel="noopener">Open the complete section ↗</a></figcaption>
</figure>

Now suppose an attacker constructs $M\neq M'$ with

$$
H(M)=H(M').
$$

For the same chosen hash algorithm,

$$
\operatorname{EMSA}_{H}(M)
=
\operatorname{EMSA}_{H}(M').
$$

A signature generated for $M$ therefore verifies for $M'$ as well. RSA may still be mathematically sound; the ambiguity enters before the RSA exponentiation. The effective security of the combined construction cannot exceed the security of its weakest component.

This does not mean that every hash collision is immediately an exploit. The attacker must arrange two usable messages and control which one is signed. <span id="definition-chosen-prefix" class="definition-target">**Chosen-prefix collisions** are particularly dangerous: the attacker first chooses two different meaningful prefixes, then constructs suffixes that make the completed messages collide</span>. But a practical collision already invalidates the clean assumption that a signed digest identifies one message.

## Reading an X.509 certificate

An <a class="concept-ref" href="#definition-x509" data-definition="X.509: the standard data model for public-key certificates.">X.509 certificate</a> has three top-level fields. <a class="concept-ref" href="#definition-rfc" data-definition="RFC: Request for Comments, a numbered publication in the Internet standards series.">RFC</a> 5280 gives their precise <a class="concept-ref" href="#definition-asn1" data-definition="ASN.1: Abstract Syntax Notation One, a language for specifying typed data structures.">ASN.1</a> structure:

<figure class="source-facsimile source-facsimile--wide">
  <div class="source-facsimile-viewport">
    <a class="source-facsimile-link" href="https://www.rfc-editor.org/rfc/rfc5280.html#section-4.1" target="_blank" rel="noopener" aria-label="Open RFC 5280 Section 4.1">
      <img src="{{ '/assets/images/source-excerpts/sha256-rfc5280-certificate.png' | relative_url }}" alt="Facsimile of RFC 5280 Section 4.1. The highlighted tbsCertificate field is followed by signatureAlgorithm and signatureValue." loading="lazy" decoding="async">
    </a>
  </div>
  <figcaption><strong>Source excerpt.</strong> RFC 5280 places <code>tbsCertificate</code>, <code>signatureAlgorithm</code> and <code>signatureValue</code> side by side. The DER encoding of <code>tbsCertificate</code> is the part the issuer signs. Yellow highlighting added. <a href="https://www.rfc-editor.org/rfc/rfc5280.html#section-4.1" target="_blank" rel="noopener">Open the complete section ↗</a></figcaption>
</figure>

<span id="definition-der" class="definition-target">**DER**, the **Distinguished Encoding Rules**, turns an ASN.1 value into one canonical sequence of bytes</span>. This matters because a signature authenticates bytes, not an abstract diagram of fields. The DER-encoded `tbsCertificate`—<span id="definition-tbs" class="definition-target">the “to be signed certificate” containing the subject, issuer, validity interval, public key and extensions</span>—is the part the issuer hashes and signs. The fields `signatureAlgorithm` and `signatureValue` tell the verifier how.

<span id="definition-tls-ipps" class="definition-target">**TLS** means **Transport Layer Security**. **IPPS** is the secure URI scheme for the **Internet Printing Protocol** carried over TLS</span>.

For

```text
sha256WithRSAEncryption
```

the words have distinct jobs:

| Component | Role |
|---|---|
| SHA-256 | hashes the encoded <a class="concept-ref" href="#definition-tbs" data-definition="tbsCertificate: the DER-encoded “to be signed” portion of an X.509 certificate."><code>tbsCertificate</code></a> |
| RSA | applies the private-key signature operation |
| X.509 | specifies the certificate fields and where the signature is stored |
| <a class="concept-ref" href="#definition-tls-ipps" data-definition="TLS is Transport Layer Security; IPPS carries the Internet Printing Protocol over TLS.">TLS/IPPS</a> | uses the certificate during a secure connection |

A self-signed certificate uses its own private key for the signature, so its subject and issuer are the same. The self-signature proves that the certificate has not been altered since that key signed it. It does **not** independently prove that the key belongs to the claimed printer or server. That requires a separate trust decision: a trusted <span id="definition-ca" class="definition-target">**certification authority** (CA), an organization or system trusted to validate identities and issue certificates</span>; <span id="definition-pinning" class="definition-target">manual **pinning**, in which a client records the expected certificate or public key directly</span>; or another authenticated enrollment mechanism. Apple explains this distinction in its [certificate-management documentation](https://support.apple.com/guide/deployment/intro-to-certificate-management-depb5eff8914/web).

For Apple clients, the choice of hash is not merely cosmetic. Apple’s published TLS certificate requirements make the migration rule explicit:

<figure class="source-facsimile source-facsimile--wide">
  <div class="source-facsimile-viewport">
    <a class="source-facsimile-link" href="https://support.apple.com/en-gb/103769" target="_blank" rel="noopener" aria-label="Open Apple’s complete requirements for trusted TLS certificates">
      <img src="{{ '/assets/images/source-excerpts/sha256-apple-tls-requirement.png' | relative_url }}" alt="Facsimile of Apple’s TLS certificate requirements. The highlighted paragraph requires a SHA-2-family certificate signature and says SHA-1-signed TLS certificates are not trusted." loading="lazy" decoding="async">
    </a>
  </div>
  <figcaption><strong>Source excerpt.</strong> Apple requires a SHA-2-family signature for trusted TLS certificates and states that SHA-1-signed TLS certificates are not trusted. This is a client trust policy, not a general diagnosis of connection failure. Yellow highlighting added. <a href="https://support.apple.com/en-gb/103769" target="_blank" rel="noopener">Open the complete guidance ↗</a></figcaption>
</figure>

An old SHA-1 certificate is therefore an independent compatibility and security problem worth removing. It is not, by itself, a diagnosis of the entire connection.

Replacing SHA-1 with SHA-256 therefore improves the collision resistance of the certificate signature and avoids a deprecated algorithm. It does not, by itself,

- turn a self-signed certificate into a publicly trusted certificate;
- extend the certificate’s validity dates;
- increase the RSA modulus size;
- encrypt application data;
- repair a network service that is not listening.

Those are separate layers.

## Where SHA-256 sits in the larger family

The names invite two common confusions.

First, SHA-1 and <span id="definition-sha2" class="definition-target">SHA-2 are different standardized designs. **SHA-2** is the family containing SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256</span>. The suffix usually names the digest length, but the internal word size and construction also matter. SHA-256 and SHA-512, for example, are not the same <a class="concept-ref" href="#definition-compression-function" data-definition="Compression function: the fixed-size state-and-block update at the core of an iterated hash.">compression function</a> with different truncation.

Second, <span id="definition-sha3" class="definition-target">**SHA-3** is a separate hash family based on the Keccak permutation</span>, not another truncation of SHA-2. It uses a <span id="definition-sponge" class="definition-target">**sponge construction**, which absorbs input into a larger internal state and then squeezes output from that state</span>. NIST standardized SHA3-224, SHA3-256, SHA3-384 and SHA3-512 in [FIPS 202](https://csrc.nist.gov/pubs/fips/202/final) as an additional family with a different internal design.

Nor should plain SHA-256 be used for every task involving a digest:

- message authentication normally uses <a class="concept-ref" href="#definition-hmac" data-definition="HMAC: Hash-based Message Authentication Code, a standard keyed construction built from a hash function.">HMAC</a> or another <a class="concept-ref" href="#definition-mac" data-definition="MAC: message-authentication code, a keyed integrity and authenticity tag.">MAC</a>, not $H(M)$ alone;
- password storage needs a deliberately expensive password-hashing construction, not fast SHA-256;
- digital signatures need a complete, correctly encoded signature scheme;
- post-quantum signature standards introduce further constructions, some of them explicitly hash-based.

“Use SHA-256” is consequently incomplete advice. The right statement is that SHA-256 is a currently approved cryptographic hash function, suitable as one component inside a protocol whose other components and encodings are also chosen correctly.

## Bitcoin: hashing and signing are still different jobs

Bitcoin is a useful example precisely because SHA-256 appears in several roles while remaining distinct from the signature algorithm.

A Bitcoin block header is an $80$-byte record containing, among other fields, the previous block hash, <span id="definition-merkle-root" class="definition-target">a **Merkle root**, the single hash-tree commitment summarizing the block’s transactions</span>, and <span id="definition-nonce" class="definition-target">a **nonce**, literally a “number used once,” which miners vary while searching for an acceptable header hash</span>. The <span id="definition-consensus-rules" class="definition-target">**consensus rules**, the validation rules that all fully validating participants must apply to agree on valid blocks</span>, apply SHA-256 twice:

$$
\operatorname{SHA256d}(x)
=
\operatorname{SHA256}(\operatorname{SHA256}(x)).
$$

The [Bitcoin block-header specification](https://developer.bitcoin.org/reference/block_chain.html#block-headers) records both the $80$-byte layout and this double-SHA-256 convention. <span id="definition-proof-of-work" class="definition-target">**Proof of work** is the search for a header whose interpreted hash is at most a network target $T$; the target determines the required difficulty</span>. Under the idealized uniform-hash model, one trial succeeds with probability

$$
p=\frac{\lfloor T\rfloor+1}{2^{256}}.
$$

If successive <a class="concept-ref" href="#definition-nonce" data-definition="Nonce: a header field miners vary to obtain different candidate hashes.">nonce</a> trials are modelled as independent, the number $N$ of trials until success is geometric:

$$
\Pr(N=k)=(1-p)^{k-1}p,
\qquad
\mathbb E[N]=\frac1p.
$$

This is a repeated preimage-style threshold search, not a birthday collision search. The double application of SHA-256 does not turn a $256$-bit output into a $512$-bit output, and it does not change the generic $2^{128}$ collision scale.

### ECDSA in one calculation

<span id="definition-ecdsa" class="definition-target">**ECDSA** means **Elliptic Curve Digital Signature Algorithm**</span>. Here the relevant points on an elliptic curve form a finite abelian group: points can be added, and $kG$ means adding the base point $G$ to itself $k$ times. Fix a point $G$ of <span id="definition-prime-order" class="definition-target">prime order $n$, meaning that $nG$ is the identity point and no smaller positive multiple of $G$ is</span>. An ECDSA private key is an integer $d\in\{1,\ldots,n-1\}$, and the corresponding public key is

$$
Q=dG.
$$

To sign a message $M$, derive an integer $z$ from its hash, choose a secret per-message value $k\in\{1,\ldots,n-1\}$, and compute

$$
R=kG,
\qquad
r=x(R)\bmod n,
\qquad
s=k^{-1}(z+rd)\bmod n.
$$

The notation $k^{-1}\bmod n$ means the <span id="definition-modular-inverse" class="definition-target">**modular inverse** of $k$: the unique residue satisfying $kk^{-1}\equiv1\pmod n$</span>. If $r=0$ or $s=0$, the signer chooses another $k$. Otherwise, the signature is the pair $(r,s)$. A verifier computes

$$
u_1=zs^{-1}\bmod n,
\qquad
u_2=rs^{-1}\bmod n,
$$

and accepts when the $x$-coordinate of

$$
u_1G+u_2Q
$$

reduces to $r$ modulo $n$. Indeed,

$$
u_1G+u_2Q
=
s^{-1}(z+rd)G
=
kG
=
R.
$$

The secret value $k$ must not be reused: two signatures with the same $k$ can reveal the private key. <span id="definition-sec" class="definition-target">The **SEC** documents are the **Standards for Efficient Cryptography** specifications published by the Standards for Efficient Cryptography Group</span>. [SEC 1, Sections 4.1.3–4.1.4](https://www.secg.org/sec1-v2.pdf#page=51) specifies the signing and verification operations. It does not prescribe one particular curve. [SEC 2, Section 2.4.1](https://www.secg.org/sec2-v2.pdf#page=13) separately specifies the field, curve, base point and order called <span id="definition-secp256k1" class="definition-target">`secp256k1`, a standardized set of parameters for a $256$-bit prime-field elliptic curve</span>. Thus **ECDSA is the signature scheme; `secp256k1` is the domain-parameter choice on which Bitcoin instantiates it**.

Transaction authorization is therefore another layer. At the mathematical level, Bitcoin historically—and still for many outputs—uses <a class="concept-ref" href="#definition-ecdsa" data-definition="ECDSA: Elliptic Curve Digital Signature Algorithm.">ECDSA</a> with the <a class="concept-ref" href="#definition-secp256k1" data-definition="secp256k1: Bitcoin’s standardized 256-bit prime-field elliptic-curve parameters."><code>secp256k1</code></a> parameters. <span id="definition-taproot" class="definition-target">**Taproot** is a Bitcoin upgrade that changed how certain spending conditions and signatures can be represented</span>. It also introduced <span id="definition-schnorr" class="definition-target">**Schnorr signatures**, a different discrete-logarithm-based signature scheme with a linear verification equation</span>, specified in <span id="definition-bip" class="definition-target">**BIP 340**; a **BIP** is a **Bitcoin Improvement Proposal**, a design or specification document for Bitcoin</span>. [BIP 340](https://bips.dev/340/) uses tagged SHA-256 internally for <span id="definition-domain-separation" class="definition-target">**domain separation**: hashing a distinct context tag with the data so that values created for one protocol purpose cannot be mistaken for values created for another</span>. SHA-256 itself is still not the signature. The same conceptual separation seen in

```text
sha256WithRSAEncryption
```

therefore reappears in a different protocol: a hash function supplies digests and challenges, while elliptic-curve algebra supplies possession of a signing key.

## What an ideal quantum computer would change

The usual quantum estimates also depend on which inverse problem is considered. [Grover search](https://arxiv.org/abs/quant-ph/9605043) reduces an unstructured preimage search from order $2^n$ to order $2^{n/2}$ quantum queries. The [Brassard–Høyer–Tapp collision algorithm](https://arxiv.org/abs/quant-ph/9705002) uses order $2^{n/3}$ queries in its <span id="definition-black-box" class="definition-target">**black-box model**, which counts calls to an ideal function while abstracting away the concrete circuit that implements it</span>. For $n=256$, these idealized exponents become $128$ for preimages and approximately $85.3$ for collisions.

These are <span id="definition-query-complexity" class="definition-target">**query-complexity** statements: they count oracle calls, not the machine’s complete running time or engineering cost</span>. They are not forecasts of a practical machine; circuit depth, error correction and quantum memory matter. In particular, the collision algorithm’s resource requirements make the slogan “quantum computers divide every hash exponent by two” false.

The more immediate conceptual contrast is with public-key cryptography. A sufficiently capable <span id="definition-fault-tolerant" class="definition-target">**fault-tolerant quantum computer**, one able to protect a long computation through quantum error correction</span>, running Shor’s algorithm would attack the number-theoretic problem behind RSA and the <span id="definition-discrete-log" class="definition-target">**discrete-logarithm problem**: recovering the scalar $d$ from $G$ and $Q=dG$</span> behind elliptic-curve signatures. It would not make SHA-256 freely invertible. A future certificate migration must therefore replace the signature primitive, not merely lengthen its hash output.

## The practical conclusion

The change

```text
sha1WithRSAEncryption
        ↓
sha256WithRSAEncryption
```

does not replace RSA by SHA-256. It keeps a public-key signature mechanism and changes the digest algorithm embedded in that mechanism.

Mathematically, the decisive scale moves from a broken $160$-bit construction whose ideal birthday bound is $2^{80}$ to a $256$-bit construction whose ideal collision scale is $2^{128}$. Operationally, it removes SHA-1 from a certificate format that modern clients may distrust or reject. Architecturally, it is still only one layer: trust, key size, validity, transport encryption and service availability must be checked separately.

The line is short, but reading it correctly requires keeping four questions separate: which hash, which signature primitive, which trust model, and which transport service.

## References

- National Institute of Standards and Technology, [*Secure Hash Standard*, FIPS 180-4](https://doi.org/10.6028/NIST.FIPS.180-4), 2015.
- National Institute of Standards and Technology, [*Digital Signature Standard*, FIPS 186-5](https://doi.org/10.6028/NIST.FIPS.186-5), 2023.
- National Institute of Standards and Technology, [*SHA-3 Standard*, FIPS 202](https://doi.org/10.6028/NIST.FIPS.202), 2015.
- Marc Stevens, Elie Bursztein, Pierre Karpman, Ange Albertini and Yarik Markov, [*The First Collision for Full SHA-1*](https://shattered.io/static/shattered.pdf), 2017.
- K. Moriarty et al., [*PKCS #1: RSA Cryptography Specifications Version 2.2*, RFC 8017](https://www.rfc-editor.org/rfc/rfc8017.html), 2016.
- D. Cooper et al., [*Internet X.509 Public Key Infrastructure Certificate and CRL Profile*, RFC 5280](https://www.rfc-editor.org/rfc/rfc5280.html), 2008.
- H. Krawczyk, M. Bellare and R. Canetti, [*HMAC: Keyed-Hashing for Message Authentication*, RFC 2104](https://www.rfc-editor.org/rfc/rfc2104.html), 1997.
- Satoshi Nakamoto, [*Bitcoin: A Peer-to-Peer Electronic Cash System*](https://bitcoin.org/bitcoin.pdf), 2008.
- Certicom Research, [*SEC 1: Elliptic Curve Cryptography*, Version 2.0, Sections 4.1.3–4.1.4](https://www.secg.org/sec1-v2.pdf#page=51), 2009.
- Certicom Research, [*SEC 2: Recommended Elliptic Curve Domain Parameters*, Version 2.0, Section 2.4.1](https://www.secg.org/sec2-v2.pdf#page=13), 2010.
- P. Wuille, J. Nick and T. Ruffing, [*BIP 340: Schnorr Signatures for secp256k1*](https://bips.dev/340/).
- L. K. Grover, [“A Fast Quantum Mechanical Algorithm for Database Search”](https://arxiv.org/abs/quant-ph/9605043), 1996.
- G. Brassard, P. Høyer and A. Tapp, [“Quantum Algorithm for the Collision Problem”](https://arxiv.org/abs/quant-ph/9705002), 1997.
- Apple, [“Available trusted root certificates for Apple operating systems” — TLS certificate requirements](https://support.apple.com/en-gb/103769).
- Apple, [“Intro to certificate management for Apple devices”](https://support.apple.com/guide/deployment/intro-to-certificate-management-depb5eff8914/web).
