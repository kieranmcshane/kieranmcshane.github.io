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

The change looks small, but it joins several different pieces of mathematics. SHA-1 and SHA-256 are hash functions, RSA is a public-key signature primitive, and an X.509 certificate is the structured object being signed. It is worth separating those roles before asking why SHA-256 is the better choice.

The printer also supplied a useful cautionary example. Its secure web service had stopped responding and came back after a restart; the old certificate itself had not expired. Replacing SHA-1 was still sensible, but it was not the explanation for every connection problem.

## Hashing is not signing

SHA-256 is a hash function, not a signature algorithm. It becomes part of a signature only when a signature scheme such as RSA signs an encoding of its output.

A fixed-output hash function is a map

$$
H:\{0,1\}^{*}\longrightarrow\{0,1\}^{n}.
$$

It accepts a bit string of arbitrary finite length and returns an $n$-bit digest. SHA-1 has $n=160$; SHA-256 has $n=256$. Both are specified in the [NIST Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final), although SHA-256 belongs to the SHA-2 family and is not simply “SHA-1 with a longer output.”

A hash function has no secret key. Anyone can compute $H(M)$, so a digest alone cannot identify the author of a message. A digital signature adds a private signing key:

$$
\sigma=\operatorname{Sign}_{sk}\!\bigl(H(M)\bigr).
$$

The verifier recomputes $H(M)$ and checks $\sigma$ with the public key $pk$. Actual schemes specify an encoding around the digest and may use randomness, but the division of labour remains:

- the hash function reduces the message to a fixed-size value;
- the signature scheme binds that value to a private key;
- the certificate binds a public key to a stated subject.

NIST therefore standardizes hash functions in [FIPS 180-4](https://doi.org/10.6028/NIST.FIPS.180-4) and signature schemes in the separate [Digital Signature Standard, FIPS 186-5](https://csrc.nist.gov/pubs/fips/186-5/final).

## Three inverse problems

The security of an ideal $n$-bit hash is usually organized around three search problems.

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

## The iterated structure

SHA-1 and SHA-256 both pad the message, divide it into $512$-bit blocks, and update a fixed-size state. In schematic form,

$$
h_0=\mathrm{IV},
\qquad
h_i=C(h_{i-1},M_i),
\qquad
H(M)=h_\ell.
$$

Here $C$ is a compression function and $M_1,\ldots,M_\ell$ are the padded blocks. This is an instance of the Merkle–Damgård pattern. The padding records the message length, so two different parses cannot be confused merely by appending zeros.

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

## What failed in SHA-1

SHA-1’s $160$-bit output would suggest a generic collision cost around $2^{80}$. Its round structure permits substantially better differential attacks. In 2017, Marc Stevens, Elie Bursztein, Pierre Karpman, Ange Albertini and Yarik Markov produced two different PDF files with exactly the same SHA-1 digest. Their [SHAttered paper](https://shattered.io/static/shattered.pdf#page=2) estimates the computation at roughly $2^{63.1}$ SHA-1 evaluations.

That result did not produce arbitrary preimages, reveal private RSA keys or invert SHA-1 in general. It did something narrower and decisive: it exhibited a practical collision for the full hash function. Collision resistance is precisely the property needed to prevent one signature from being transferred between two messages with the same digest.

NIST had already discouraged SHA-1 for signature generation before the public collision. It now plans to [remove SHA-1 from all remaining applications by the end of 2030](https://csrc.nist.gov/News/2022/nist-transitioning-away-from-sha-1-for-all-apps). SHA-256 remains an approved member of SHA-2. No accepted practical collision attack is known for the full $64$-step SHA-256 function; published attacks concern reduced or otherwise modified versions.

## How a collision crosses into RSA

For a concrete model, consider `RSASSA-PKCS1-v1_5`. Let

$$
N=pq,
\qquad
ed\equiv1\pmod{\lambda(N)}.
$$

The private exponent is $d$ and the public exponent is $e$. The standard does not exponentiate the raw hash. It first builds a precisely formatted encoded message

$$
\operatorname{EM}=\operatorname{EMSA}_{H}(M),
$$

containing padding and an ASN.1 `DigestInfo` value that identifies $H$. The signature is

$$
s\equiv \operatorname{EM}^{\,d}\pmod N,
$$

and verification checks that

$$
s^e\equiv \operatorname{EMSA}_{H}(M)\pmod N.
$$

The exact signature procedure is given in [Section 8.2 of PKCS #1](https://www.rfc-editor.org/rfc/rfc8017.html#section-8.2); its message encoding is specified separately in [Section 9.2](https://www.rfc-editor.org/rfc/rfc8017.html#section-9.2).

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

This does not mean that every hash collision is immediately an exploit. The attacker must arrange two usable messages and control which one is signed. Chosen-prefix collisions are particularly dangerous because they allow the two messages to begin differently. But a practical collision already invalidates the clean assumption that a signed digest identifies one message.

## Reading an X.509 certificate

An X.509 certificate has the simplified form

```text
Certificate  ::=  SEQUENCE {
    tbsCertificate       TBSCertificate,
    signatureAlgorithm   AlgorithmIdentifier,
    signatureValue       BIT STRING
}
```

This structure appears in [Section 4.1 of RFC 5280](https://www.rfc-editor.org/rfc/rfc5280.html#section-4.1). The `tbsCertificate`—“to be signed certificate”—contains the subject, issuer, validity interval, public key and extensions. The issuer hashes and signs that structure. The fields `signatureAlgorithm` and `signatureValue` tell the verifier how.

For

```text
sha256WithRSAEncryption
```

the words have distinct jobs:

| Component | Role |
|---|---|
| SHA-256 | hashes the encoded `tbsCertificate` |
| RSA | applies the private-key signature operation |
| X.509 | specifies the certificate fields and where the signature is stored |
| TLS/IPPS | uses the certificate during a secure connection |

A self-signed certificate uses its own private key for the signature, so its subject and issuer are the same. The self-signature proves that the certificate has not been altered since that key signed it. It does **not** independently prove that the key belongs to the claimed printer or server. That requires a separate trust decision: a trusted certification authority, manual pinning, or another authenticated enrollment mechanism. Apple explains this distinction in its [certificate-management documentation](https://support.apple.com/guide/deployment/intro-to-certificate-management-depb5eff8914/web).

For Apple clients, the choice of hash is not merely cosmetic. Apple’s [published TLS certificate requirements](https://support.apple.com/en-gb/103769) state that trusted TLS server certificates must use SHA-2 and that SHA-1-signed TLS certificates are no longer trusted. This does not mean that every local connection failure is caused by SHA-1; it means that an old SHA-1 certificate is an independent compatibility and security problem worth removing.

Replacing SHA-1 with SHA-256 therefore improves the collision resistance of the certificate signature and avoids a deprecated algorithm. It does not, by itself,

- turn a self-signed certificate into a publicly trusted certificate;
- extend the certificate’s validity dates;
- increase the RSA modulus size;
- encrypt application data;
- repair a network service that is not listening.

Those are separate layers.

## Where SHA-256 sits in the larger family

The names invite two common confusions.

First, SHA-1 and SHA-2 are different standardized designs. SHA-2 includes SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224 and SHA-512/256. The suffix usually names the digest length, but the internal word size and construction also matter. SHA-256 and SHA-512, for example, are not the same compression function with different truncation.

Second, SHA-3 is not another truncation of SHA-2. It is based on the Keccak permutation and a sponge construction. NIST standardized SHA3-224, SHA3-256, SHA3-384 and SHA3-512 in [FIPS 202](https://csrc.nist.gov/pubs/fips/202/final) as an additional family with a different internal design.

Nor should plain SHA-256 be used for every task involving a digest:

- message authentication normally uses HMAC or another MAC, not $H(M)$ alone;
- password storage needs a deliberately expensive password-hashing construction, not fast SHA-256;
- digital signatures need a complete, correctly encoded signature scheme;
- post-quantum signature standards introduce further constructions, some of them explicitly hash-based.

“Use SHA-256” is consequently incomplete advice. The right statement is that SHA-256 is a currently approved cryptographic hash function, suitable as one component inside a protocol whose other components and encodings are also chosen correctly.

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
- Apple, [“Available trusted root certificates for Apple operating systems” — TLS certificate requirements](https://support.apple.com/en-gb/103769).
- Apple, [“Intro to certificate management for Apple devices”](https://support.apple.com/guide/deployment/intro-to-certificate-management-depb5eff8914/web).
