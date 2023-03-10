// TODO https://reactrouter.com/docs/en/v6/getting-started/tutorial#using-a-bundler
// export default function App() {
//   return (
//     <div>
//       <h1>Bookkeeper!</h1>
//     </div>
//   );
// }

// TODO https://reactrouter.com/docs/en/v6/getting-started/tutorial#connect-the-url
// import { Link } from "react-router-dom";

// export default function App() {
//   return (
//     <div>
//       <h1>Bookkeeper</h1>
//       <nav
//         style={{
//           borderBottom: "solid 1px",
//           paddingBottom: "1rem",
//         }}
//       >
//         <Link to="/invoices">Invoices</Link> |{" "}
//         <Link to="/expenses">Expenses</Link>
//       </nav>
//     </div>
//   );
// }

// TODO https://reactrouter.com/docs/en/v6/getting-started/tutorial#nested-routes
// import { Outlet, Link } from "react-router-dom";

// export default function App() {
//   return (
//     <div>
//       <h1>Bookkeeper</h1>
//       <nav
//         style={{
//           borderBottom: "solid 1px",
//           paddingBottom: "1rem",
//         }}
//       >
//         <Link to="/invoices">Invoices</Link> |{" "}
//         <Link to="/expenses">Expenses</Link>
//       </nav>
//       <Outlet />
//     </div>
//   );
// }

// ! YOUR CODE STARTS HERE
// TODO ESLINT OVERRIDES
/* eslint-disable jsx-a11y/anchor-is-valid */
/* eslint-disable no-script-url */
/* eslint-disable jsx-a11y/role-supports-aria-props */
/* eslint-disable jsx-a11y/img-redundant-alt */

import { useEffect } from 'react';
import { Link } from "react-router-dom";

export default function Landing() {
	// useEffect(() => {
        // const stylesheets = [
		// 	'https://fonts.googleapis.com/css?family=IBM+Plex+Sans:400,600',
		// 	'/static/solid/dist/css/style.css',
        // ]
		// stylesheets.forEach(element => {
        //     // TODO https://stackoverflow.com/questions/28386125/dynamically-load-a-stylesheet-with-react
        //     var head = document.head;
        //     var link = document.createElement("link");

        //     link.type = "text/css";
        //     link.rel = "stylesheet";
        //     link.href = element;

        //     head.appendChild(link);

        //     return () => { head.removeChild(link); }
		// });

        // const scripts_head = [
		// 	'https://unpkg.com/animejs@3.0.1/lib/anime.min.js',
        //     'https://unpkg.com/scrollreveal@4.0.0/dist/scrollreveal.min.js'
		// ]
		// scripts_head.forEach(element => {
		// 	const script = document.createElement('script');

		// 	script.src = element;
		// 	// script.async = true;
		
		// 	document.head.appendChild(script);
		
		// 	return () => {
		// 	  document.head.removeChild(script);
		// 	}
		// });

		// const scripts = [
		// 	'/static/solid/dist/js/main.min.js',
		// ]
		// scripts.forEach(element => {
		// 	const script = document.createElement('script');

		// 	script.src = element;
		// 	// script.async = true;
		
		// 	document.body.appendChild(script);
		
		// 	return () => {
		// 	  document.body.removeChild(script);
		// 	}
		// });
	//   });

  return (
    <div className="body-wrap">
        <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Sans:400,600" rel="stylesheet"/>
        <link rel="stylesheet" href="/static/solid/dist/css/style.css"/>
        <script src="https://unpkg.com/animejs@3.0.1/lib/anime.min.js"></script>
        <script src="https://unpkg.com/scrollreveal@4.0.0/dist/scrollreveal.min.js"></script>

        <header className="site-header">
            <div className="container">
                <div className="site-header-inner">
                    <div className="brand header-brand">
                        <h1 className="m-0">
							<a href="#">
								<img className="header-logo-image" src="/static/solid/dist/images/logo.svg" alt="Logo"/>
                            </a>
                        </h1>
                    </div>
                </div>
            </div>
        </header>

        <main>
            <section className="hero">
                <div className="container">
                    <div className="hero-inner">
						<div className="hero-copy">
	                        <h1 className="hero-title mt-0">"Cop" up with the future</h1>
	                        <p className="hero-paragraph">We have envisioned the future of the police service. Want to see what it's about?</p>
	                        <div className="hero-cta"><Link to="vps" className="button button-primary">Open VPS</Link><a className="button" href="#">Get in touch</a></div>
						</div>
						<div className="hero-figure anime-element">
							<svg className="placeholder" width="528" height="396" viewBox="0 0 528 396">
								<rect width="528" height="396" style={{ fill:'transparent' }} />
							</svg>
							<div className="hero-figure-box hero-figure-box-01" data-rotation="45deg"></div>
							<div className="hero-figure-box hero-figure-box-02" data-rotation="-45deg"></div>
							<div className="hero-figure-box hero-figure-box-03" data-rotation="0deg"></div>
							<div className="hero-figure-box hero-figure-box-04" data-rotation="-135deg"></div>
							<div className="hero-figure-box hero-figure-box-05"></div>
							<div className="hero-figure-box hero-figure-box-06"></div>
							<div className="hero-figure-box hero-figure-box-07"></div>
							<div className="hero-figure-box hero-figure-box-08" data-rotation="-22deg"></div>
							<div className="hero-figure-box hero-figure-box-09" data-rotation="-52deg"></div>
							<div className="hero-figure-box hero-figure-box-10" data-rotation="-50deg"></div>
						</div>
                    </div>
                </div>
            </section>

            <section className="features section">
                <div className="container">
					<div className="features-inner section-inner has-bottom-divider">
                        <div className="features-wrap">
                            <div className="feature text-center is-revealing">
                                <div className="feature-inner">
                                    <div className="feature-icon">
										<img src="/static/solid/dist/images/feature-icon-01.svg" alt="Feature 01"/>
                                    </div>
                                    <h4 className="feature-title mt-24">Be Productive</h4>
                                    <p className="text-sm mb-0">Fermentum posuere urna nec tincidunt praesent semper feugiat nibh. A arcu cursus vitae congue mauris. Nam at lectus urna duis convallis. Mauris rhoncus aenean vel elit scelerisque mauris.</p>
                                </div>
                            </div>
							<div className="feature text-center is-revealing">
                                <div className="feature-inner">
                                    <div className="feature-icon">
										<img src="/static/solid/dist/images/feature-icon-02.svg" alt="Feature 02"/>
                                    </div>
                                    <h4 className="feature-title mt-24">Be Productive</h4>
                                    <p className="text-sm mb-0">Fermentum posuere urna nec tincidunt praesent semper feugiat nibh. A arcu cursus vitae congue mauris. Nam at lectus urna duis convallis. Mauris rhoncus aenean vel elit scelerisque mauris.</p>
                                </div>
                            </div>
                            <div className="feature text-center is-revealing">
                                <div className="feature-inner">
                                    <div className="feature-icon">
										<img src="/static/solid/dist/images/feature-icon-03.svg" alt="Feature 03"/>
                                    </div>
                                    <h4 className="feature-title mt-24">Be Productive</h4>
                                    <p className="text-sm mb-0">Fermentum posuere urna nec tincidunt praesent semper feugiat nibh. A arcu cursus vitae congue mauris. Nam at lectus urna duis convallis. Mauris rhoncus aenean vel elit scelerisque mauris.</p>
                                </div>
                            </div>
                            <div className="feature text-center is-revealing">
                                <div className="feature-inner">
                                    <div className="feature-icon">
										<img src="/static/solid/dist/images/feature-icon-04.svg" alt="Feature 04"/>
                                    </div>
                                    <h4 className="feature-title mt-24">Be Productive</h4>
                                    <p className="text-sm mb-0">Fermentum posuere urna nec tincidunt praesent semper feugiat nibh. A arcu cursus vitae congue mauris. Nam at lectus urna duis convallis. Mauris rhoncus aenean vel elit scelerisque mauris.</p>
                                </div>
                            </div>
							<div className="feature text-center is-revealing">
                                <div className="feature-inner">
                                    <div className="feature-icon">
										<img src="/static/solid/dist/images/feature-icon-05.svg" alt="Feature 05"/>
                                    </div>
                                    <h4 className="feature-title mt-24">Be Productive</h4>
                                    <p className="text-sm mb-0">Fermentum posuere urna nec tincidunt praesent semper feugiat nibh. A arcu cursus vitae congue mauris. Nam at lectus urna duis convallis. Mauris rhoncus aenean vel elit scelerisque mauris.</p>
                                </div>
                            </div>
                            <div className="feature text-center is-revealing">
                                <div className="feature-inner">
                                    <div className="feature-icon">
										<img src="/static/solid/dist/images/feature-icon-06.svg" alt="Feature 06"/>
                                    </div>
                                    <h4 className="feature-title mt-24">Be Productive</h4>
                                    <p className="text-sm mb-0">Fermentum posuere urna nec tincidunt praesent semper feugiat nibh. A arcu cursus vitae congue mauris. Nam at lectus urna duis convallis. Mauris rhoncus aenean vel elit scelerisque mauris.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section className="pricing section">
                <div className="container-sm">
                    <div className="pricing-inner section-inner">
                        <div className="pricing-header text-center">
                            <h2 className="section-title mt-0">Unlimited for all</h2>
                            <p className="section-paragraph mb-0">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut ad quis nostrud.</p>
                        </div>
						<div className="pricing-tables-wrap">
                            <div className="pricing-table">
                                <div className="pricing-table-inner is-revealing">
                                    <div className="pricing-table-main">
                                        <div className="pricing-table-header pb-24">
                                            <div className="pricing-table-price"><span className="pricing-table-price-currency h2">$</span><span className="pricing-table-price-amount h1">49</span><span className="text-xs">/month</span></div>
                                        </div>
										<div className="pricing-table-features-title text-xs pt-24 pb-24">What you will get</div>
                                        <ul className="pricing-table-features list-reset text-xs">
                                            <li>
                                                <span>Lorem ipsum dolor sit nisi</span>
                                            </li>
                                            <li>
                                                <span>Lorem ipsum dolor sit nisi</span>
                                            </li>
                                            <li>
                                                <span>Lorem ipsum dolor sit nisi</span>
                                            </li>
											<li>
												<span>Lorem ipsum dolor sit nisi</span>
											</li>
                                        </ul>
                                    </div>
                                    <div className="pricing-table-cta mb-8">
                                        <a className="button button-primary button-shadow button-block" href="#">Pre order now</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

			<section className="cta section">
				<div className="container">
					<div className="cta-inner section-inner">
						<h3 className="section-title mt-0">Want to be part of the revolution?</h3>
						<div className="cta-cta">
							<a className="button button-primary button-wide-mobile" href="#">Get in touch</a>
						</div>
					</div>
				</div>
			</section>
        </main>

        <footer className="site-footer">
            <div className="container">
                <div className="site-footer-inner">
                    <div className="brand footer-brand">
						<a href="#">
							<img className="header-logo-image" src="/static/solid/dist/images/logo.svg" alt="Logo"/>
						</a>
                    </div>
                    <ul className="footer-links list-reset">
                        <li>
                            <a href="#">Contact</a>
                        </li>
                        <li>
                            <a href="#">About us</a>
                        </li>
                        <li>
                            <a href="#">FAQ's</a>
                        </li>
                        <li>
                            <a href="#">Support</a>
                        </li>
                    </ul>
                    <ul className="footer-social-links list-reset">
                        <li>
                            <a href="#">
                                <span className="screen-reader-text">Facebook</span>
                                <svg width="16" height="16" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M6.023 16L6 9H3V6h3V4c0-2.7 1.672-4 4.08-4 1.153 0 2.144.086 2.433.124v2.821h-1.67c-1.31 0-1.563.623-1.563 1.536V6H13l-1 3H9.28v7H6.023z" fill="#0270D7"/>
                                </svg>
                            </a>
                        </li>
                        <li>
                            <a href="#">
                                <span className="screen-reader-text">Twitter</span>
                                <svg width="16" height="16" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M16 3c-.6.3-1.2.4-1.9.5.7-.4 1.2-1 1.4-1.8-.6.4-1.3.6-2.1.8-.6-.6-1.5-1-2.4-1-1.7 0-3.2 1.5-3.2 3.3 0 .3 0 .5.1.7-2.7-.1-5.2-1.4-6.8-3.4-.3.5-.4 1-.4 1.7 0 1.1.6 2.1 1.5 2.7-.5 0-1-.2-1.5-.4C.7 7.7 1.8 9 3.3 9.3c-.3.1-.6.1-.9.1-.2 0-.4 0-.6-.1.4 1.3 1.6 2.3 3.1 2.3-1.1.9-2.5 1.4-4.1 1.4H0c1.5.9 3.2 1.5 5 1.5 6 0 9.3-5 9.3-9.3v-.4C15 4.3 15.6 3.7 16 3z" fill="#0270D7"/>
                                </svg>
                            </a>
                        </li>
                        <li>
                            <a href="#">
                                <span className="screen-reader-text">Google</span>
                                <svg width="16" height="16" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M7.9 7v2.4H12c-.2 1-1.2 3-4 3-2.4 0-4.3-2-4.3-4.4 0-2.4 2-4.4 4.3-4.4 1.4 0 2.3.6 2.8 1.1l1.9-1.8C11.5 1.7 9.9 1 8 1 4.1 1 1 4.1 1 8s3.1 7 7 7c4 0 6.7-2.8 6.7-6.8 0-.5 0-.8-.1-1.2H7.9z" fill="#0270D7"/>
                                </svg>
                            </a>
                        </li>
                    </ul>
                    <div className="footer-copyright">&copy; 2017 - 2022 IE Solutions, all rights reserved</div>
                </div>
            </div>
        </footer>

        <script src="/static/solid/dist/css/style.css"></script>
    </div>
  );
}