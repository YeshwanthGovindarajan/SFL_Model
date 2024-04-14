import unittest
from your_module import SFL  

class TestSFL(unittest.TestCase):

    def setUp(self):
        self.sfl = SFL()
        self.sfl.initialize()

    def test_initialization(self):
        self.assertTrue(isinstance(self.sfl.global_model, dict))
        self.assertEqual(len(self.sfl.global_model['weights']), 10)
        self.assertEqual(len(self.sfl.blockchain), 1)
        self.assertEqual(self.sfl.blockchain[0]['details'], 'Genesis block')

    def test_global_model_initial_weights(self):
        for weight in self.sfl.global_model['weights']:
            self.assertGreaterEqual(weight, 0)
            self.assertLessEqual(weight, 1)

    def test_mint_nft_correct_signature_and_token(self):
        user_details = "Alice"
        nft = self.sfl.mint_nft(user_details)
        self.assertTrue(all(key in nft for key in ['signature', 'user_data', 'token_id']))
        self.assertEqual(nft['user_data']['user_details'], user_details)
        self.assertIsNotNone(nft['signature'])
        self.assertRegex(nft['token_id'], '^[a-f0-9]{64}$')  

    def test_digital_twin_creation_timestamp(self):
        participant_id = "Bob"
        self.sfl.create_digital_twin_transaction(participant_id)
        twin = self.sfl.digital_twins[participant_id]
        self.assertTrue(isinstance(twin['timestamp'], float))

    def test_authenticate_user_not_already_authenticated(self):
        participant_id = "Charlie"
        result = self.sfl.authenticate_user(participant_id)
        self.assertTrue(result)
        self.assertIn(participant_id, self.sfl.authenticated_users)

    def test_authenticate_user_already_authenticated(self):
        participant_id = "Charlie"
        self.sfl.authenticate_user(participant_id)
        result = self.sfl.authenticate_user(participant_id)
        self.assertFalse(result)

    def test_submit_model_update_not_authenticated_user(self):
        participant_id = "Dana"
        model_update = self.sfl.prepare_model_update(participant_id)
        result = self.sfl.submit_model_update(participant_id, model_update)
        self.assertFalse(result)

    def test_submit_model_update_authenticated_user(self):
        participant_id = "Charlie"
        self.sfl.authenticate_user(participant_id)
        model_update = self.sfl.prepare_model_update(participant_id)
        result = self.sfl.submit_model_update(participant_id, model_update)
        self.assertTrue(result)
        self.assertEqual(self.sfl.blockchain[-1]['participant_id'], participant_id)

    def test_validate_blockchain_corrupted_chain(self):
        participant_id = "Charlie"
        self.sfl.authenticate_user(participant_id)
        model_update = self.sfl.prepare_model_update(participant_id)
        self.sfl.submit_model_update(participant_id, model_update)
        # Simulate corruption
        self.sfl.blockchain[-1]['preceding_digest'] = "corrupted_data"
        is_valid = self.sfl.validate_blockchain()
        self.assertFalse(is_valid)

    def test_model_aggregation_and_benchmarking(self):
        participants = ["Charlie", "Dave"]
        for participant in participants:
            self.sfl.authenticate_user(participant)
            self.sfl.submit_model_update(participant, self.sfl.prepare_model_update(participant))
        aggregated_model = self.sfl.model_aggregation()
        is_benchmark_ok = self.sfl.digital_twin_benchmarking(aggregated_model)
        self.assertTrue(is_benchmark_ok)

    def test_significant_model_change_detected(self):
        self.sfl.global_model['weights'] = [0.5] * 10
        self.sfl.blockchain = [{'model_update': [0.6] * 10}]  
        aggregated_model = self.sfl.model_aggregation()
        is_benchmark_ok = self.sfl.digital_twin_benchmarking(aggregated_model)
        self.assertFalse(is_benchmark_ok)

if __name__ == '__main__':
    unittest.main()
