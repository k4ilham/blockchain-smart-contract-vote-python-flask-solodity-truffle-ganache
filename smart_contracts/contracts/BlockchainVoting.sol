// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BlockchainVoting {
    struct Voter {
        bool isRegistered;
        bool hasVoted;
        uint vote;
    }

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    address public admin;
    mapping(address => Voter) public voters;
    Candidate[] public candidates;
    uint public totalVotes;

    enum VoteStatus { Valid, DoubleVote }
    mapping(address => VoteStatus) public voteStatus;

    // List of registered voters' addresses
    address[] public registeredVoters;

    event VoterRegistered(address voter);
    event VoteCast(address voter, uint candidateId);
    event VoteInvalid(address voter);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier onlyRegistered() {
        require(voters[msg.sender].isRegistered, "Voter is not registered");
        _;
    }

    constructor(string[] memory candidateNames) {
        admin = msg.sender;
        for (uint i = 0; i < candidateNames.length; i++) {
            candidates.push(Candidate({
                id: i,
                name: candidateNames[i],
                voteCount: 0
            }));
        }
    }

    // Register a voter
    function registerVoter(address voter) external onlyAdmin {
        require(!voters[voter].isRegistered, "Voter is already registered");
        voters[voter] = Voter({
            isRegistered: true,
            hasVoted: false,
            vote: 0
        });
        registeredVoters.push(voter);  // Add to registered voters list
        emit VoterRegistered(voter);
    }

    // Cast a vote
    function castVote(uint candidateId) external onlyRegistered {
        require(!voters[msg.sender].hasVoted, "Voter has already voted");
        require(candidateId < candidates.length, "Invalid candidate ID");

        // Check for double voting
        if (voters[msg.sender].hasVoted) {
            voteStatus[msg.sender] = VoteStatus.DoubleVote;
            emit VoteInvalid(msg.sender);
            return;
        }

        voters[msg.sender].vote = candidateId;
        voters[msg.sender].hasVoted = true;
        candidates[candidateId].voteCount += 1;
        totalVotes += 1;

        emit VoteCast(msg.sender, candidateId);
    }

    // Get candidates' details
    function getCandidates() external view returns (Candidate[] memory) {
        return candidates;
    }

    // Get vote status of a voter
    function getVoteStatus(address voter) external view returns (VoteStatus) {
        return voteStatus[voter];
    }

    // Get total votes for a candidate
    function getCandidateVotes(uint candidateId) external view returns (uint) {
        require(candidateId < candidates.length, "Invalid candidate ID");
        return candidates[candidateId].voteCount;
    }

    // Fungsi untuk menangani deteksi suara ganda
    function detectDoubleVote(address voter) public view returns (string memory) {
        // Periksa status suara untuk pemilih
        if (voters[voter].hasVoted && voteStatus[voter] == VoteStatus.DoubleVote) {
            return "Double Vote Detected";
        } else {
            return "Valid Vote";
        }
    }

    // Function to retrieve the admin address
    function getAdmin() external view returns (address) {
        return admin;
    }

    // Function to get the list of registered voters
    function getVoterList() external view returns (address[] memory) {
        return registeredVoters;
    }

}
