"""
Validateurs de données
"""

class DataValidator:
    
    @staticmethod
    def validate_positive(value, name):
        """Vérifie qu'une valeur est positive"""
        if value <= 0:
            raise ValueError(f"{name} doit être > 0")
        return True
    
    @staticmethod
    def validate_range(value, min_val, max_val, name):
        """Vérifie qu'une valeur est dans une plage"""
        if not (min_val <= value <= max_val):
            raise ValueError(f"{name} doit être entre {min_val} et {max_val}")
        return True
    
    @staticmethod
    def validate_temperature(temp):
        """Vérifie la température"""
        if temp <= -273.15:
            raise ValueError("Température doit être > -273.15°C")
        return True
    
    @staticmethod
    def validate_input_data(data):
        """Valide toutes les données d'entrée"""
        errors = []
        
        try:
            DataValidator.validate_temperature(data.get('T', 20))
        except ValueError as e:
            errors.append(str(e))
        
        try:
            DataValidator.validate_positive(data.get('rho', 1000), "Masse volumique")
        except ValueError as e:
            errors.append(str(e))
        
        try:
            DataValidator.validate_positive(data.get('Q', 0.05), "Débit")
        except ValueError as e:
            errors.append(str(e))
        
        if errors:
            raise ValueError("\n".join(errors))
        
        return True