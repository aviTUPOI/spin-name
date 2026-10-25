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
sha256sums=('d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed  release.tar.gz')

package() {
    cd "$pkgname-$pkgver"
    install -Dm755 spin-name.py "$pkgdir/usr/bin/spin-name"
}
