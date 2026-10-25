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
sha256sums=('cd73e187852e92f9b5d2401a1594b165ee3404d9de403acd6cd2947e7b2c4875')

package() {
    cd "$pkgname-$pkgver"
    install -Dm755 spin-name.py "$pkgdir/usr/bin/spin-name"
}
