Updates - Oct 16, 2025
----------------------



Cooling Vape Juice Update
=========================

* Since our last meeting we have validated additional predictions from our VLM pipeline for detecting cooling e-cigarette juices.
* We have now verified 500 predictions with only 7 of those being incorrect, this results in a 98.6% accuracy.
* Up to this point all of these products have been from a single website, vape.com.
* In order to have a more robust test of the pipeline we are expanding to other websites to see how that impacts our results.
* We are bringing in additional samples from Perfect Vape, Vaping.com, Vapesourcing, and CSVape.
* This additional data will not only increase our sample size but introduce some variance from how these websites are formatted and what information they provide.







Expanding Cooling Flavor Detection
==================================


* Upon further review of websites and data, I do believe there is an opportunity to apply this method to disposable e-cigarettes.
* The only issue I see is that our object detection network is not going to be able to distinguish between disposable and re-usable e-cigarettes.
* Thus, we will need to scrape sites only for disposables that we know will come pre-loaded with a e-cigarette juice flavor.
* In our database we have already tagged products with this category and should be able to use that data.
* This would expand the detection from e-cigarette juices to disposable e-cigarettes to see how the performance compares.





