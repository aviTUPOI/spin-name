# Maintainer: avi <bebrailibobro@gmail.com>
pkgname=spin-name
pkgver=2
pkgrel=1
pkgdesc="3D ASCII rotating logo generator for the terminal (vibe-coded)"
arch=('any')
url="https://github.com/aviTUPOI/spin-name"
license=('MIT')
depends=('python')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('0e7d87459b8653ad6960b58f3327e17c61b9b259b43933dc78ba6243051f1d15')

package() {
    cd "$pkgname-$pkgver"
    install -Dm755 spin-name.py "$pkgdir/usr/bin/spin-name"
}
