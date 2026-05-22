# Alennusperusteiden ekosysteemi

Täältä löytyvät Findynetin tukeman erityisryhmien alennusperusteiden luottamusekosysteemin todisteiden määrittelyt.

## Todisteiden rakenne

Eläkeläistodisteen `vct`-määritys löytyy tiedostosta [credentials/v2/PensionCredentialVCT.json](credentials/v2/PensionCredentialVCT.json).

## Ulkoasumääritykset

Eläkeläistodisteen SVG-malline löytyy tiedostosta [templates/svg/PensionCredential_v2_fi.svg](templates/svg/PensionCredential_v2_fi.svg). (Kieliversiot [PensionCredential_v2_en.svg](templates/svg/PensionCredential_v2_en.svg) ja [PensionCredential_v2_sv.svg](templates/svg/PensionCredential_v2_sv.svg).)

## Esimerkit

Esimerkki eläkeläistodisteesta JWT-muodossa löytyy tiedostosta [examples/sd-jwt-vc/pensioncredential.jwt](examples/sd-jwt-vc/pensioncredential.jwt). Sen sisältöä voi tarkastella esimerkiksi palvelussa [jwt.io](https://jwt.io).

Esimerkki todisteen myöntäjän `issuer metadata` -asetuksista löytyy tiedostosta [examples/openid-credential-issuer.json](examples/openid-credential-issuer.json).
