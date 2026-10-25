# Maintainer: avi <bebrailibobro@gmail.com>
pkgname=spin-name
pkgver=1.0.0
pkgrel=1
pkgdesc="3D ASCII rotating logo generator for the terminal (vibe-coded)"
arch=('any')
url="https://github.com/aviTUPOI/spin-name"
license=('MIT')
depends=('python')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('204b586e54eb2fcfcfef65644fb9310d62393484f7f4701ee40dccfa6016e180')

package() {
    cd "$pkgname-$pkgver"
    install -Dm755 spin-name.py "$pkgdir/usr/bin/spin-name"
}
