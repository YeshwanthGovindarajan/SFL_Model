// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SFLBlockchain is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    struct ModelUpdate {
        uint index;
        uint timestamp;
        string participantId;
        float modelUpdate;
        string precedingDigest;
        string credential;
        string details;
    }

    mapping(uint256 => ModelUpdate) public modelUpdates;

    event BlockSubmitted(uint index, string participantId, float modelUpdate);

    constructor() ERC721("SFLModelToken", "SFLT") {}

    function createGenesisBlock() public onlyOwner {
        ModelUpdate memory genesisBlock = ModelUpdate({
            index: 0,
            timestamp: block.timestamp,
            participantId: "",
            modelUpdate: 0,
            precedingDigest: "0",
            credential: "",
            details: "Genesis Block"
        });
        modelUpdates[0] = genesisBlock;
        _tokenIds.increment();
    }

    function submitModelUpdate(string memory participantId, float modelUpdate, string memory credential, string memory details) public returns (uint) {
        uint256 currentId = _tokenIds.current();
        ModelUpdate memory previousBlock = modelUpdates[currentId - 1];
        ModelUpdate memory newBlock = ModelUpdate({
            index: currentId,
            timestamp: block.timestamp,
            participantId: participantId,
            modelUpdate: modelUpdate,
            precedingDigest: generateDigest(previousBlock),
            credential: credential,
            details: details
        });

        modelUpdates[currentId] = newBlock;
        emit BlockSubmitted(newBlock.index, newBlock.participantId, newBlock.modelUpdate);
        
        _tokenIds.increment();
        return currentId;
    }

    function generateDigest(ModelUpdate memory block) private pure returns (string memory) {
        return keccak256(abi.encodePacked(block.timestamp, block.precedingDigest, block.details));
    }

    function validateBlockchain() public view returns (bool) {
        for (uint i = 1; i < _tokenIds.current(); i++) {
            ModelUpdate memory currentBlock = modelUpdates[i];
            ModelUpdate memory previousBlock = modelUpdates[i - 1];

            if (keccak256(abi.encodePacked(currentBlock.precedingDigest)) != keccak256(abi.encodePacked(generateDigest(previousBlock)))) {
                return false;
            }
        }
        return true;
    }
}
