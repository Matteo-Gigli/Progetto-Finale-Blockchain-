# Progetto-Finale-Blockchain-

A customer commissions the company you work for a platform to manage the sale of some goods at auction.

Each auction has a certain duration, and users of the platform can place any amount on any auction still in progress.

The company's CTO asks you to develop the foundation of this platform, using Redis as the main database. In fact, imagine that the platform could generate a lot of attention and be used by an ever-increasing number of users who may require having to scale horizontally to hold traffic.

He therefore wants to use a very fast database to manage the various bids, and then store the outcome of the auction, like all other user data, on a relational database.

For the purposes of what it asks you to do, just set up DJango to use the default sqlite database.

In summary, the CTO asks you to use DJango with a normal relational database, and to use Redis only to manage the various bids of each auction.

At the end of each auction, in addition to storing the information on the relational database, it generates a JSON file containing all the details of the auction and references to the winner. Then calculate the hash of this JSON and write it in a transaction on the Ethereum (Ropsten) blockchain.

All other choices are at your discretion. Show that you are able to structure this project in the best way to complete the training path.
