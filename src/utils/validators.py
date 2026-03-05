from datetime import datetime, date, time

class Validators:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        return '@' in email and '.' in email.split('@')[-1]
    
    @staticmethod
    def validate_future_date(fecha):
        """Validate if date is in the future"""
        today = date.today()
        return fecha >= today
    
    @staticmethod
    def validate_business_hours(hora):
        """Validate if time is within business hours (9:00-18:00)"""
        start_time = time(9, 0)
        end_time = time(18, 0)
        return start_time <= hora <= end_time
    
    @staticmethod
    def validate_service(servicio):
        """Validate service type"""
        valid_services = ['Corte', 'Tinte', 'Afeitado', 'Peinado']
        return servicio in valid_services
    
    @staticmethod
    def validate_reservation_status(estado):
        """Validate reservation status"""
        valid_states = ['Pendiente', 'Confirmada', 'Cancelada', 'Completada']
        return estado in valid_states
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """Validate required fields exist and are not empty"""
        missing = [field for field in required_fields if field not in data]
        empty = [field for field in required_fields if field in data and not str(data[field]).strip()]
        return missing, empty