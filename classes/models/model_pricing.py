import logging

class ModelPricing:
    """Handles pricing calculations for different AI models."""
    
    # Pricing per 1M tokens (input, output)
    MODEL_PRICES = {
        "gpt-4.1-mini": (0.40, 1.60)
    }
    
    @classmethod
    def calculate_cost(cls, model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate the cost of an API call based on the model and token usage."""
        if model_name not in cls.MODEL_PRICES:
            logging.error(f"Pricing not available for model: {model_name}")
            return 0.0
            
        input_price, output_price = cls.MODEL_PRICES[model_name]
        input_cost = (input_tokens * input_price) / 1_000_000
        output_cost = (output_tokens * output_price) / 1_000_000
        
        return round(input_cost + output_cost, 8)