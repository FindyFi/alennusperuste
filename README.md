# Alennusperusteiden ekosysteemi

Täältä löytyvät Findynetin tukeman erityisryhmien alennusperusteiden luottamusekosysteemin todisteiden määrittelyt.

## Todisteiden rakenne

Eläkeläistodisteen `vct`-määritys löytyy tiedostosta [credentials/v1/PensionCredentialVCT.json](credentials/v1/PensionCredentialVCT.json).

## Ulkoasumääritykset

Eläkeläistodisteen SVG-malline löytyy tiedostosta [templates/svg/PensionCredential_v1_fi.svg](templates/svg/PensionCredential_v1_fi.svg). (Kieliversiot [PensionCredential_v1_en.svg](templates/svg/PensionCredential_v1_en.svg) ja [PensionCredential_v1_sv.svg](templates/svg/PensionCredential_v1_sv.svg).)

## Esimerkit

Esimerkki eläkeläistodisteesta JWT-muodossa löytyy tiedostosta [examples/sd-jwt-vc/pensioncredential.jwt](examples/sd-jwt-vc/pensioncredential.jwt). Sen sisältöä voi tarkastella esimerkiksi palvelussa [jwt.io](https://jwt.io).

Esimerkki todisteen myöntäjän `issuer metadata` -asetuksista löytyy tiedostosta [examples/openid-credential-issuer.json](examples/openid-credential-issuer.json).