const SFLBlockchain = artifacts.require("SFLBlockchain");

contract("SFLBlockchain", accounts => {
    let sflInstance;

    before(async () => {
        sflInstance = await SFLBlockchain.deployed();
    });

    it("should create the genesis block correctly", async () => {
        await sflInstance.createGenesisBlock({from: accounts[0]});
        const genesisBlock = await sflInstance.modelUpdates(0);
        assert.equal(genesisBlock.index.toNumber(), 0, "Genesis block should have index 0");
        assert.equal(genesisBlock.details, "Genesis Block", "Incorrect details for genesis block");
    });

    it("should allow submission of new model updates", async () => {
        const participantId = "Participant1";
        const modelUpdate = 0.123;
        const credential = "Credential1";
        const details = "Model update 1";

        await sflInstance.submitModelUpdate(participantId, modelUpdate, credential, details, {from: accounts[1]});
        const block = await sflInstance.modelUpdates(1);
        
        assert.equal(block.index.toNumber(), 1, "Block index should be 1");
        assert.equal(block.participantId, participantId, "Incorrect participant ID");
        assert.equal(block.details, details, "Incorrect block details");
    });

    it("should validate the blockchain integrity", async () => {
        const isValid = await sflInstance.validateBlockchain();
        assert.isTrue(isValid, "Blockchain should be valid after valid transactions");
    });

    it("should detect invalid blockchain state", async () => {
        await sflInstance.testInvalidateBlock(1, "tamperedDigest", {from: accounts[0]});
        const isValid = await sflInstance.validateBlockchain();
        assert.isFalse(isValid, "Blockchain should be invalid after tampering");
    });
});
