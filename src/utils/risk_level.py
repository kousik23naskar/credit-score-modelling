# src/utils/risk_level.py

def get_risk_level(default_prob: float) -> str:
    """
    Determine risk level based on default probability.
    
    Args:
        default_prob (float): The predicted default probability (0 to 1).

    Returns:
        str: Risk level (Very Low, Low, Medium, High, Very High)

    Raises:
        ValueError: If default_prob is not a float or not in [0, 1].
    """
    try:
        if not isinstance(default_prob, (float, int)):
            raise TypeError("default_prob must be a number (float or int).")

        if not (0.0 <= default_prob <= 1.0):
            raise ValueError("default_prob must be between 0.0 and 1.0.")

        if default_prob < 0.1:
            return "Very Low"
        elif default_prob < 0.3:
            return "Low"
        elif default_prob < 0.5:
            return "Medium"
        elif default_prob < 0.7:
            return "High"
        else:
            return "Very High"

    except Exception as e:
        raise ValueError(f"Invalid input for risk level calculation: {e}")
