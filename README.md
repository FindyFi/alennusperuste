# Alennusperusteiden ekosysteemi

Täältä löytyvät Findynetin tukeman erityisryhmien alennusperusteiden luottamusekosysteemin todisteiden määrittelyt.

## Todisteiden rakenne

Eläkeläistodisteen `vct`-määritys löytyy tiedostosta [credentials/v3/PensionCredentialVCT.json](credentials/v3/PensionCredentialVCT.json).

## Ulkoasumääritykset

Eläkeläistodisteen SVG-malline löytyy tiedostosta [templates/svg/PensionCredential_v3_fi.svg](templates/svg/PensionCredential_v3_fi.svg). (Kieliversiot [PensionCredential_v3_en.svg](templates/svg/PensionCredential_v3_en.svg) ja [PensionCredential_v3_sv.svg](templates/svg/PensionCredential_v3_sv.svg).)

## Esimerkit

Esimerkki eläkeläistodisteesta JWT-muodossa löytyy tiedostosta [examples/sd-jwt-vc/pensioncredential-v3.jwt](examples/sd-jwt-vc/pensioncredential-v3.jwt). Sen sisältöä voi tarkastella esimerkiksi palvelussa [jwt.io](https://jwt.io).

Esimerkki todisteen myöntäjän `issuer metadata` -asetuksista löytyy tiedostosta [examples/openid-credential-issuer-v3.json](examples/openid-credential-issuer-v3.json).
