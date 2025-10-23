from bs4 import BeautifulSoup
import re

vape_sourcing = '''<div class="accordion-menu">
                    <div class="level-1">
                        <div class="title">
                            <a href="/featured.html">
                                <span>New Vapes</span>
                            </a>
                        </div>
                    </div>
                    <div class="level-1 menu-clearance">
                        <div class="title has-sub-menu">
                            <a href="/clearance.html">
                                <span class="show-color">Clearance</span>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list">
                                    <ul>
                                        <li><a href="/mystery-box.html">Mystery Box</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/buy-one-get-one.html">Buy One Get One</a></li>
                                        <li><a href="/disposables-under-10.html">Disposables Under $10</a></li>
                                        
                                        <li><a href="/clearance-disposables.html">Disposables Clearance</a></li>
                                        <li><a href="/clearance-vape-kits.html">Clearance Vape Kits</a></li>
                                        <li class="special"><a href="/crazy-sale.html">Crazy Sale</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/clearance-atomizer-tank.html">Clearance Atomizer / Tank</a></li>
                                        <li><a href="/clearance-vape-juice.html">Clearance Vape Juice</a></li>
                                        <li><a href="/clearance-vaporizers.html">Clearance Vaporizers</a></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="menu-banner banner-type-1">
                                <ul>
                                                                            <li>    
                                            <a href="https://vapesourcing.com/disposables-under-10.html">
                                                <div class="image">
                                                    <img width="570" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202403/disposable-under-_10.jpg" alt="Disposables Under $10" title="Disposables Under $10" src="https://image.vapesourcing.com/images/202403/disposable-under-_10.jpg">
                                                </div>
                                                <p>Disposables Under $10</p>
                                            </a>
                                        </li>
                                                                            <li>    
                                            <a href="https://vapesourcing.com/clearance-vape-kits.html">
                                                <div class="image">
                                                    <img width="570" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202506/clearance-vape-banner-285-188.jpg" alt="Clearance Vape Kit" title="Clearance Vape Kit">
                                                </div>
                                                <p>Clearance Vape Kit</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1">
                        <div class="title has-sub-menu">
                            <a href="/brand.html">
                                <span>Brand</span>
                            </a>
                        </div>
                        <div class="sub-menu brand-content">
                            <div class="brand-menu">
                                <ul>
                                    <li class="active">Vapes</li>
                                    <li>Juice</li>
                                </ul>
                                <span class="more"><a href="/brand.html">All Brand <i class="icon iconfont iconUP-copy"></i></a></span>
                            </div>
                            
                            <div class="brand-logo">
                                <ul class="active">
                                                                            <li>
                                            <a href="/smok.html">
                                                <img width="216" height="82" title="SMOK" alt="SMOK" class="lazyload" data-src="/images/202102/SMOK.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/uwell.html">
                                                <img width="216" height="82" title="Uwell" alt="Uwell" class="lazyload" data-src="/images/202102/Uwell.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/raz.html">
                                                <img width="216" height="82" title="RAZ" alt="RAZ" class="lazyload" data-src="https://image.vapesourcing.com/images/202412/raz-216-82.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/geek-vape.html">
                                                <img width="216" height="82" title="Geek Vape" alt="Geek Vape" class="lazyload" data-src="/images/202102/Geek_Vape.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/joyetech.html">
                                                <img width="216" height="82" title="Joyetech" alt="Joyetech" class="lazyload" data-src="/images/202102/Joyetech.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/voopoo.html">
                                                <img width="216" height="82" title="VOOPOO" alt="VOOPOO" class="lazyload" data-src="/images/202102/VOOPOO.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/vaporesso.html">
                                                <img width="216" height="82" title="Vaporesso" alt="Vaporesso" class="lazyload" data-src="/images/202102/Vaporesso.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/flum.html">
                                                <img width="216" height="82" title="Flum" alt="Flum" class="lazyload" data-src="https://image.vapesourcing.com/images/202306/FLUM-LOGO.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/eleaf.html">
                                                <img width="216" height="82" title="Eleaf" alt="Eleaf" class="lazyload" data-src="/images/202102/Eleaf.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/geek-bar.html">
                                                <img width="216" height="82" title="GEEK BAR" alt="GEEK BAR" class="lazyload" data-src="https://image.vapesourcing.com/images/202207/GEEKBAR.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/lost-vape.html">
                                                <img width="216" height="82" title="Lost Vape" alt="Lost Vape" class="lazyload" data-src="/images/202102/Lost_Vape.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/hellvape.html">
                                                <img width="216" height="82" title="Hellvape" alt="Hellvape" class="lazyload" data-src="/images/202102/hellvape.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/vandy-vape.html">
                                                <img width="216" height="82" title="Vandy Vape" alt="Vandy Vape" class="lazyload" data-src="/images/202102/Vandy_Vape.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/nexa.html">
                                                <img width="216" height="82" title="NEXA" alt="NEXA" class="lazyload" data-src="https://image.vapesourcing.com/images/202502/nexa-216-82.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/innokin.html">
                                                <img width="216" height="82" title="Innokin" alt="Innokin" class="lazyload" data-src="/images/202102/Innokin.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/ijoy.html">
                                                <img width="216" height="82" title="IJOY" alt="IJOY" class="lazyload" data-src="/images/202102/IJOY.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/lost-mary.html">
                                                <img width="216" height="82" title="Lost Mary" alt="Lost Mary" class="lazyload" data-src="https://image.vapesourcing.com/images/202306/Lost_Mary_logo_2023.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/freemax.html">
                                                <img width="216" height="82" title="FreeMax" alt="FreeMax" class="lazyload" data-src="/images/202007/freemax3.png">
                                            </a>
                                        </li>
                                                                    </ul>
                                <ul>
                                                                            <li>
                                            <a href="/naked-100.html">
                                                <img width="216" height="82" title="Naked 100" alt="Naked 100" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Naked_100_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/pod-juice.html">
                                                <img width="216" height="82" title="Pod Juice" alt="Pod Juice" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Pod_Juice_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/i-love-salts.html">
                                                <img width="216" height="82" title="I Love Salts" alt="I Love Salts" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/i_love_salts_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/blvk-unicorn.html">
                                                <img width="216" height="82" title="BLVK Unicorn" alt="BLVK Unicorn" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/BLVK_Unicorn_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/juice-head.html">
                                                <img width="216" height="82" title="Juice Head" alt="Juice Head" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Juice_Head_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/twist-salt.html">
                                                <img width="216" height="82" title="Twist Salt" alt="Twist Salt" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Twist_Salt_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/finest.html">
                                                <img width="216" height="82" title="The Finest" alt="The Finest" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Finest_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/vapetasia.html">
                                                <img width="216" height="82" title="Vapetasia" alt="Vapetasia" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Vapetasia_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/candy-king.html">
                                                <img width="216" height="82" title="Candy King" alt="Candy King" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Candy_King_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/coastal-clouds.html">
                                                <img width="216" height="82" title="Coastal Clouds" alt="Coastal Clouds" class="lazyload" data-src="https://image.vapesourcing.com/images/202302/coastal_clouds.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/skwezed.html">
                                                <img width="216" height="82" title="SKWEZED" alt="SKWEZED" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/SKWEZED_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/cloud-nurdz.html">
                                                <img width="216" height="82" title="Cloud Nurdz" alt="Cloud Nurdz" class="lazyload" data-src="https://image.vapesourcing.com/images/202302/cloud_nurdz.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/pachamama.html">
                                                <img width="216" height="82" title="Pachamama" alt="Pachamama" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Pachamama_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/vape-7-daze.html">
                                                <img width="216" height="82" title="Vape 7 Daze" alt="Vape 7 Daze" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Vape_7_Daze_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/innevape.html">
                                                <img width="216" height="82" title="Innevape" alt="Innevape" class="lazyload" data-src="https://image.vapesourcing.com/images/202302/innevape.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/hi-drip.html">
                                                <img width="216" height="82" title="Hi Drip" alt="Hi Drip" class="lazyload" data-src="https://image.vapesourcing.com/images/202302/hi_drip.png">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/jam-monster.html">
                                                <img width="216" height="82" title="Jam Monster" alt="Jam Monster" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Jam_Monster_logo.jpg">
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="/sadboy.html">
                                                <img width="216" height="82" title="Sadboy" alt="Sadboy" class="lazyload" data-src="https://image.vapesourcing.com/images/202111/Sadboy_logo.jpg">
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1 menu-disposables">
                        <div class="title has-sub-menu">
                            <a href="/disposable-pod.html">
                                <span style="float:left;">Disposables</span>
                                <i class="icon iconfont iconsale-6"></i>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list">
                                    <div class="title"><a href="/puffs-vape.html">Puffs Vape</a></div>
                                    <ul class="active">
                                        <li><a href="/60000-puffs.html">≥60000 Puffs</a></li>
                                        <li><a href="/50000-puffs.html">≥50000 Puffs</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/40000-puffs.html">≥40000 Puffs</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/30000-puffs.html">≥30000 Puffs</a></li>
                                        <li><a href="/25000-puffs.html">≥25000 Puffs</a></li>
                                        <li><a href="/20000-puffs.html">≥20000 Puffs</a></li>
                                        <li><a href="/15000-puffs.html">≥15000 Puffs</a></li>
                                        <li><a href="/10000-puffs.html">≥10000 Puffs</a></li>
                                    </ul>
                                </div>
                                <div class="list third-level top-spacing">
                                    <div class="title"><a href="/disposable-flavors.html">Disposable Flavors</a></div>
                                    <ul>
                                        <li><a href="/ice-vapes.html">Ice Vapes</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/sour-flavor-disposable-vapes.html">Sour Flavor Vapes</a></li>
                                        <li><a href="/cotton-candy-disposable-vape.html">Cotton Candy</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/tobacco-flavor-disposable-vape.html">Tobacco Flavors</a></li>
                                        <li><a href="/clear-flavor-vapes.html">Clear Flavor Vapes</a></li>
                                        <li><a href="/fruit-flavor-disposable-vape.html">Fruit Flavors</a></li>
                                        <li><a href="/dessert-flavor-disposable-vape.html">Dessert Flavors</a></li>
                                    </ul>
                                </div>
                                <div class="list third-level">
                                    <div class="title">View All Disposables</div>
                                    <ul>
                                        <li><a href="/rechargeable-disposable.html">Rechargeable</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/disposable-vape-with-screen.html">Disposable Vape with Screen</a></li>
                                        <li><a href="/low-nicotine-vape.html">Low Nicotine Vape</a></li>
                                        <li><a href="/nicotine-free-vape.html">Nicotine Free Vape</a></li>
                                        <li><a href="/multi-use-disposable-vape.html">Multi Use Disposable Vape</a></li>
                                        <li><a href="/smart-phone-disposable-vapes.html">Smart Phone Disposable Vapes</a></li>
                                        <li><a href="/flavor-control-vapes.html">Flavor Control Vapes</a></li>
                                        <li><a href="/disposable-hookah.html">Disposable Hookah</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/disposables-bundle.html">Disposables Bundle Pack</a></li>
                                        <li><a href="/disposable-vape-with-double-tanks.html">Disposable Vape with Double Tanks</a></li>
                                        <li><a href="/disposable-vape-with-detachable-battery.html">Disposable Vape with Detachable Battery</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/multi-buy.html">Multi Buy</a></li>
                                    </ul>
                                </div>
                                <div class="list third-level">
                                    <div class="title"><a href="/disposable-vape-brands.html">Disposable Brands</a></div>
                                    <ul>
                                        <li><a href="/ploox.html">Ploox</a></li><a href="/ploox.html">
                                        </a><li><a href="/ploox.html"></a><a href="/lost-mary.html">Lost Mary</a></li>
                                        <li><a href="/geek-bar.html">Geek Bar</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/olit.html">Olit</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/raz.html">RAZ</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/foger.html">Foger</a></li>
                                        <li><a href="/mr-fog.html">Mr Fog</a></li>
                                        <li><a href="/kado-bar.html">Kado Bar</a></li>
                                        <li><a href="/flum.html">Flum Vape</a></li>
                                        <li><a href="/nexa.html">NEXA</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/adjust-vape.html">Adjust Vape</a></li>
                                        <li><a href="/fume-vape.html">Fume Vape</a></li>
                                        <li><a href="/vozol.html">Vozol</a></li>
                                        <li><a href="/off-stamp-vape.html">Off Stamp Vape</a></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="menu-banner banner-type-2">
                                <ul>
                                                                            <li>
                                            <a href="https://vapesourcing.com/oxbar-astro-maze-50k.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202504/OXBAR-Astro-Maze-50K-285-188.jpg" alt="OXBAR Astro Maze 50K" title="OXBAR Astro Maze 50K" src="https://image.vapesourcing.com/images/202504/OXBAR-Astro-Maze-50K-285-188.jpg">
                                                </div>
                                                <p>OXBAR Astro Maze 50K</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/nexa-pix-35k.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202508/nexa-pix-285-188.jpg" alt="NEXA PIX 35K" title="NEXA PIX 35K" src="https://image.vapesourcing.com/images/202508/nexa-pix-285-188.jpg">
                                                </div>
                                                <p>NEXA PIX 35K</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/lost-angel-mate-50k.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202506/lost-angel-mate-50k-285-188.jpg" alt="Lost Angel Mate 50K" title="Lost Angel Mate 50K" src="https://image.vapesourcing.com/images/202506/lost-angel-mate-50k-285-188.jpg">
                                                </div>
                                                <p>Lost Angel Mate 50K</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/flum-ut-bar-50000.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202504/flum-ut-bar-50k-285-188.jpg" alt="Flum UT Bar 50K" title="Flum UT Bar 50K" src="https://image.vapesourcing.com/images/202504/flum-ut-bar-50k-285-188.jpg">
                                                </div>
                                                <p>Flum UT Bar 50K</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1">
                        <div class="title has-sub-menu">
                            <a href="/starter-kit.html">
                                <span>Vape Kit</span>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list">
                                    <ul>
                                                                                    <li>
                                                <a href="/refillable-vape.html">Refillable Vape</a>
                                            </li>
                                                                                    <li>
                                                <a href="/boro-kit.html">Boro Kit</a>
                                            </li>
                                                                                    <li>
                                                <a href="/pod-system-kit.html">Pod Systems</a>
                                            </li>
                                                                                    <li>
                                                <a href="/mod-pod-kits.html">Pod Mods Kits</a>
                                            </li>
                                                                                    <li>
                                                <a href="/vape-mod-kits.html">Vape Mod Kits</a>
                                            </li>
                                                                                    <li>
                                                <a href="/vape-pen-kits.html">Vape Pen Kits</a>
                                            </li>
                                                                                    <li>
                                                <a href="/clearance-vape-kits.html">Clearance Vape Kits</a>
                                            </li>
                                                                                <li>
                                            <a href="/disposable-pod.html">Disposable Pod Kits</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="menu-banner banner-type-2">
                                <ul>
                                                                            <li>
                                            <a href="https://vapesourcing.com/geekvape-aegis-hero-5-kit.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202508/geekvape-aegis-hero-5-285-188.jpg" alt="Geekvape Aegis Hero 5" title="Geekvape Aegis Hero 5">
                                                </div>
                                                <p>Geekvape Aegis Hero 5</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/uwell-caliburn-g4-pro-kit.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202507/uwell-caliburn-g4-pro-285-188.jpg" alt="Uwell Caliburn G4 Pro" title="Uwell Caliburn G4 Pro">
                                                </div>
                                                <p>Uwell Caliburn G4 Pro</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/geekvape-aegis-legend-5-kit.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202506/geekvape-aegis-legend-5-285-188.jpg" alt="Geekvape Aegis Legend 5" title="Geekvape Aegis Legend 5">
                                                </div>
                                                <p>Geekvape Aegis Legend 5</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/uwell-caliburn-g4-kit.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202504/uwell-caliburn-g4-285-188.jpg" alt="Uwell Caliburn G4" title="Uwell Caliburn G4">
                                                </div>
                                                <p>Uwell Caliburn G4</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1">
                        <div class="title has-sub-menu">
                            <a href="/e-juice.html">
                                <span>E-liquid</span>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list third-level">
                                    <div class="title">All E-Liquids</div>
                                    <ul>
                                        <li><a href="/fruits-flavor-e-juice.html">Fruit Flavors E-Juice</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/sweet-flavor-e-juice.html">Dessert Flavors</a></li>
                                        <li><a href="/menthol-flavor-e-juice.html">Menthol Flavors</a></li>
                                        <li><a href="/tobacco-flavor-e-juice.html">Tobacco Flavors</a></li>
                                        <li><a href="/salt-nic.html">Nicotine Salts E-Liquids</a></li>
                                        <li><a href="/0-mg-e-juice.html">Nicotine Free Vape Juice</a></li>
                                        <li><a href="/20-60-mg-e-juice.html">60mg Vape Juice</a></li>
                                        <li><a href="/3-12-mg-e-juice.html">12mg Vape Juice</a></li>
                                    </ul>
                                </div>
                                <div class="list third-level">
                                    <div class="title">E-Liquids Brands</div>
                                    <ul>
                                        <li><a href="/naked-100.html">Naked 100</a></li>
                                        <li><a href="/pod-juice.html">Pod Juice</a></li>
                                        <li><a href="/raz.html">Raz Vape</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/lost-mary.html">Lost Mary</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/i-love-salts.html">I Love Salts</a></li>
                                        <li><a href="/blvk-unicorn.html">BLVK Unicorn</a></li>
                                        <li><a href="/juice-head.html">Juice Head</a></li>
                                        <li><a href="/twist-salt.html">Twist Salt</a></li>
                                        <li><a href="/finest.html">The Finest</a></li>
                                        <li><a href="/vapetasia.html">Vapetasia</a></li>
                                        <li><a href="/candy-king.html">Candy King</a></li>
                                        <li><a href="/mad-hatter.html">Mad Hatter</a></li>
                                        <li><a href="/skwezed.html">Skwezed</a></li>
                                    </ul>
                                </div>
                            </div>

                            <div class="menu-banner banner-type-2">
                                <ul>
                                                                            <li>
                                            <a href="https://vapesourcing.com/naked-100-euro-gold-e-juice-60ml.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/imagecache/c/images/202403/euro-gold-naked-100.jpg" alt="Naked 100 Euro Gold" title="Naked 100 Euro Gold">
                                                </div>
                                                <p>Naked 100 Euro Gold</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/raz.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202410/raz-e-juice-285-188.jpg" alt="RAZ x Pod Juice E-liquid" title="RAZ x Pod Juice E-liquid">
                                                </div>
                                                <p>RAZ x Pod Juice E-liquid</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/naked-100-tobacco-american-patriot-e-juice-60ml.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/imagecache/c/images/202403/american-patriot-naked-100.jpg" alt="Naked 100 American Patriot" title="Naked 100 American Patriot">
                                                </div>
                                                <p>Naked 100 American Patriot</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/tropic-mango-ice-urban-tale-e-juice-30ml.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202506/285-188-tropic-mango-icce-urban-tale.jpg" alt="Tropic Mango Ice Urban Tale E-juice" title="Tropic Mango Ice Urban Tale E-juice">
                                                </div>
                                                <p>Tropic Mango Ice Urban Tale E-juice</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1">
                        <div class="title has-sub-menu">
                            <a href="/battery-device.html">
                                <span>Mod</span>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list">
                                    <ul>
                                                                                    <li>
                                                <a href="/box-mod.html">Box Mods</a>
                                            </li>
                                                                                    <li>
                                                <a href="/mechanical-mods.html">Mechanical Mods</a>
                                            </li>
                                                                                    <li>
                                                <a href="/dna-vape-mod.html">DNA Vape Mod</a>
                                            </li>
                                                                                    <li>
                                                <a href="/squonk-mod.html">Squonk Mods</a>
                                            </li>
                                                                                    <li>
                                                <a href="/built-in-battery-mods.html">Built-In Battery Mods</a>
                                            </li>
                                                                                    <li>
                                                <a href="/boro-mod.html">Boro Mod</a>
                                            </li>
                                                                                    <li>
                                                <a href="/high-end-mods.html">High Power Vape Mods 150w+</a>
                                            </li>
                                                                            </ul>
                                </div>
                            </div>
                            <div class="menu-banner banner-type-2">
                                <ul>
                                                                            <li>
                                            <a href="https://vapesourcing.com/timesvape-the-dreamer-clutch-mod.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202407/Timesvape.jpg" alt="Timesvape The Dreamer Clutch Mechanical Mod" title="Timesvape The Dreamer Clutch Mechanical Mod" src="https://image.vapesourcing.com/images/202407/Timesvape.jpg">
                                                </div>
                                                <p>Timesvape The Dreamer Clutch Mechanical Mod</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/vandy-vape-pulse-aio-v2-kit.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202311/AIO-V2-285188.jpg" alt="Vandy Vape Pulse AIO V2" title="Vandy Vape Pulse AIO V2" src="https://image.vapesourcing.com/images/202311/AIO-V2-285188.jpg">
                                                </div>
                                                <p>Vandy Vape Pulse AIO V2</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/voopoo-drag-5-box-mod.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202407/VOOPOO-Drag-5-Box-Mod-285188.jpg" alt="VOOPOO Drag 5 Box Mod" title="VOOPOO Drag 5 Box Mod">
                                                </div>
                                                <p>VOOPOO Drag 5 Box Mod</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/lost-vape-centaurus-bt200-box-mod.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202507/lost-vape-centaurus-bt200-mod-285-188.jpg" alt="Lost Vape Centaurus BT200 Box Mod" title="Lost Vape Centaurus BT200 Box Mod">
                                                </div>
                                                <p>Lost Vape Centaurus BT200 Box Mod</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1">
                        <div class="title has-sub-menu">
                            <a href="/atomizer-tank.html">
                                <span>Atomizer</span>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list third-level">
                                    <div class="title">Rebuildables</div>
                                    <ul>
                                                                                    <li>
                                                <a href="/rda.html">RDA</a>
                                            </li>
                                                                                    <li>
                                                <a href="/rta.html">RTA</a>
                                            </li>
                                                                                    <li>
                                                <a href="/rdta.html">RDTA</a>
                                            </li>
                                                                                    <li>
                                                <a href="/boro-tank.html">Boro Tank</a>
                                            </li>
                                                                            </ul>
                                </div>
                                <div class="list third-level">
                                    <div class="title">Tanks</div>
                                    <ul>
                                                                                    <li><a href="/sub-ohm-tank.html">Sub Ohm Tank</a></li>
                                                                                    <li><a href="/mesh-tank.html">Mesh Coil Tank</a></li>
                                                                                    <li><a href="/mouth-to-lung-tank.html">MTL Tank</a></li>
                                                                                    <li><a href="/replacement-pod-and-cartridge.html">Pod Cartridge</a></li>
                                                                            </ul>
                                </div>
                            </div>
                            <div class="menu-banner banner-type-2">
                                <ul>
                                                                            <li>
                                            <a href="https://vapesourcing.com/thunderhead-creations-blaze-max-rta.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202408/thunderhead-creations-blaze-max-rta-285-188.jpg" alt="Thunderhead Creations Blaze Max RTA" title="Thunderhead Creations Blaze Max RTA" src="https://image.vapesourcing.com/images/202408/thunderhead-creations-blaze-max-rta-285-188.jpg">
                                                </div>
                                                <p>Thunderhead Creations Blaze Max RTA</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/hellvape-fat-rabbit-solo-2-rta.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202411/hellvape-fat-rabbit-2-solo-rta-285-188.jpg" alt="Hellvape Fat Rabbit Solo 2 RTA" title="Hellvape Fat Rabbit Solo 2 RTA" src="https://image.vapesourcing.com/images/202411/hellvape-fat-rabbit-2-solo-rta-285-188.jpg">
                                                </div>
                                                <p>Hellvape Fat Rabbit Solo 2 RTA</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/hellvape-dead-rabbit-3-rta-joker-edition.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202504/hellvape-dead-rabbit-3-rta-joker-285-188.jpg" alt="Hellvape Dead Rabbit 3 RTA Joker Edition" title="Hellvape Dead Rabbit 3 RTA Joker Edition" src="https://image.vapesourcing.com/images/202504/hellvape-dead-rabbit-3-rta-joker-285-188.jpg">
                                                </div>
                                                <p>Hellvape Dead Rabbit 3 RTA Joker Edition</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/vaporesso-xros-series-corex-3-pod-cartridge.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202507/vaporesso-xros-series-pod-285-188.jpg" alt="corex 3.0 pods" title="corex 3.0 pods" src="https://image.vapesourcing.com/images/202507/vaporesso-xros-series-pod-285-188.jpg">
                                                </div>
                                                <p>corex 3.0 pods</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1">
                        <div class="title has-sub-menu">
                            <a href="/accessories.html">
                                <span>Accessory</span>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list">
                                    <ul>
                                                                                    <li>
                                                <a href="/nicotine-pouches.html">Nicotine Pouches</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/nicotine-strips.html">Nicotine Strips</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/nicotine-gum.html">Nicotine Gum</a> 
                                                                                                    <i class="icon iconfont iconsale-6"></i>
                                                                                            </li>
                                                                                    <li>
                                                <a href="/batterycell.html">Battery Cell</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/replacement-glass-tube.html">Glass Tubes</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/replacement-coils-heads.html">Coils/Heads</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/charger.html">Chargers</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/wire-wick-tool.html">Rebuildable Tools</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/drip-tip.html">Drip Tips</a> 
                                                                                            </li>
                                                                                    <li>
                                                <a href="/other-accessories.html">Others</a> 
                                                                                            </li>
                                                                            </ul>
                                </div>
                            </div>
                            <div class="menu-banner banner-type-2 banner-type-3">
                                <ul>
                                                                            <li>
                                            <a href="https://vapesourcing.com/zyn.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202406/ZYN-285188.jpg" alt="ZYN Nicotine Pouches" title="ZYN Nicotine Pouches">
                                                </div>
                                                <p>ZYN Nicotine Pouches</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/g-pulse-nicotine-pouches.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202506/G-Pulse-Nicotine-Pouches-285188.jpg" alt="G-Pulse Nicotine Pouches" title="G-Pulse Nicotine Pouches">
                                                </div>
                                                <p>G-Pulse Nicotine Pouches</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/lucy.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202508/Lucy-285188-2.jpg" alt="Lucy Nicotine Pouches &amp; Gums" title="Lucy Nicotine Pouches &amp; Gums">
                                                </div>
                                                <p>Lucy Nicotine Pouches &amp; Gums</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/melta.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202502/Nicotine-Strips-285-188.jpg" alt="Melta Nicotine Strips" title="Melta Nicotine Strips">
                                                </div>
                                                <p>Melta Nicotine Strips</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/slapple-nicotine-gum.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202507/slapple-nicotine-gum-285-188.jpg" alt="Slapple Nicotine Gum" title="Slapple Nicotine Gum">
                                                </div>
                                                <p>Slapple Nicotine Gum</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/mates-brand-pouchmate-nicotine-pouches.html">
                                                <div class="image">
                                                    <img width="285" height="188" class="lazyload" data-src="https://image.vapesourcing.com/images/202507/mates-brand-pouchmate-285-188.jpg" alt="Mates Brand PouchMate Nicotine Pouches" title="Mates Brand PouchMate Nicotine Pouches">
                                                </div>
                                                <p>Mates Brand PouchMate Nicotine Pouches</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    <div class="level-1">
                        <div class="title has-sub-menu">
                            <a href="/vaporizers.html">
                                <span>Vaporizer</span>
                            </a>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list third-level">
                                    <div class="title">Vaporizer Brands</div>
                                    <ul>
                                        <li><a href="/yocan.html">Yocan</a></li>
                                        <li><a href="/doteco.html">Doteco</a></li>
                                        <li><a href="/ccell.html">Ccell</a></li>
                                        <li><a href="/lookah.html">Lookah</a></li>
                                        <li><a href="/hamilton-devices.html">Hamilton Devices</a></li>
                                        <li><a href="/puffco.html">Puffco</a><i class="icon iconfont iconsale-6"></i></li>
                                        <li><a href="/ltq-vapor.html">ltq Vapor</a></li>
                                        <li><a href="/ploox.html">Ploox</a></li>
                                    </ul>
                                </div>
                                <div class="list third-level">
                                    <div class="title">All Vaporizer</div>
                                    <ul>
                                                                                    <li>
                                                <a href="/wax.html">Wax vaporizers</a>
                                            </li>
                                                                                    <li>
                                                <a href="/dry-herb.html">Dry herb vaporizers</a>
                                            </li>
                                                                                    <li>
                                                <a href="/510-thread-battery.html">510 Thread Battery</a>
                                            </li>
                                                                                    <li>
                                                <a href="/vapor-cup.html">Cup Vapes</a>
                                            </li>
                                                                                <li>
                                            <a href="/bongs-water-pipes.html">Bongs &amp; Water Pipes</a>
                                        </li>
                                        <li>
                                            <a href="/dab-rig.html">Dab Rig</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="menu-banner banner-type-2">
                                <ul>
                                                                            <li>
                                            <a href="https://vapesourcing.com/the-kind-pen-bullet-2-vaporizer.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202507/the-kind-pen-bullet-2-285-188.jpg" alt="The Kind Pen Bullet 2.0" title="The Kind Pen Bullet 2.0" src="https://image.vapesourcing.com/images/202507/the-kind-pen-bullet-2-285-188.jpg">
                                                </div>
                                                <p>The Kind Pen Bullet 2.0</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/yocan-deuce-510-thread-battery.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202506/yocan-deuce-285-188.jpg" alt="Yocan Deuce 510 Thread Battery" title="Yocan Deuce 510 Thread Battery" src="https://image.vapesourcing.com/images/202506/yocan-deuce-285-188.jpg">
                                                </div>
                                                <p>Yocan Deuce 510 Thread Battery</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/iecigbest-tobor-electric-dab-rig.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202507/IECIGBEST-Tobor-285-188.jpg" alt="IECIGBEST Tobor Electric Dab Rig" title="IECIGBEST Tobor Electric Dab Rig" src="https://image.vapesourcing.com/images/202507/IECIGBEST-Tobor-285-188.jpg">
                                                </div>
                                                <p>IECIGBEST Tobor Electric Dab Rig</p>
                                            </a>
                                        </li>
                                                                            <li>
                                            <a href="https://vapesourcing.com/ploox-nest-portable-hookah.html">
                                                <div class="image">
                                                    <img width="285" height="188" class=" lazyloaded" data-src="https://image.vapesourcing.com/images/202507/ploox-nest-285188.jpg" alt="Ploox Nest Portable Hookah" title="Ploox Nest Portable Hookah" src="https://image.vapesourcing.com/images/202507/ploox-nest-285188.jpg">
                                                </div>
                                                <p>Ploox Nest Portable Hookah</p>
                                            </a>
                                        </li>
                                                                    </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="level-1">
                        <div class="title">
                            <a href="/best-vape.html">
                                <span>Best</span>
                            </a>
                        </div>
                    </div>
                    <div class="level-1 d-lg-none">
                        <div class="title">
                            <a href="/coupons.html">
                                <span>Coupons</span>
                            </a>
                        </div>
                    </div>
                    <div class="level-1 d-lg-none">
                        <div class="title has-sub-menu">
                            <span>Country Website</span>
                        </div>
                        <div class="sub-menu">
                            <div class="menu-list">
                                <div class="list">
                                    <ul>
                                        <li>
                                            <a href="https://vapesourcing.uk/">English(UK)</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="level-1 d-lg-none">
                        <div class="title">
                            <a href="/contacts">
                                <span>Contact us</span>
                            </a>
                        </div>
                    </div>
                </div>'''

def csvape():
    with open('scraping/prep/csvape.html', 'r') as rf:
        html_content = rf.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)

    collection_links = [link['href'] for link in links if '/collections/' in link['href']]

    print(collection_links)

def run_vapesourcing():
    html_content = vape_sourcing
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)

    collection_links = [link['href'] for link in links]

    print(collection_links)


if __name__ == "__main__":
    run_vapesourcing()
