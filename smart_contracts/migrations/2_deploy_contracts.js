const BlockchainVoting = artifacts.require("BlockchainVoting");

module.exports = function (deployer) {
    deployer.deploy(BlockchainVoting, ["Alice", "Bob", "Charlie"]); // Daftar kandidat
};
