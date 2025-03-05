# Initializing a FastAPI Project

## 1. Create a FastAPI App
```python
app = FastAPI()
```
This creates a new FastAPI application instance.

## 2. Database Setup (SQLAlchemy)
```python
engine = create_engine(URL_DATABASE)
```
Sets up a connection to the database using SQLAlchemy.
SQLAlchemy ORM queries are synchronous

## 3. Create a Session Factory
```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```
Creates a session factory for database interactions.

## 4. Define the Base Class for Models
```python
Base = declarative_base()
```
Defines the base class for all SQLAlchemy models.

## 5. Create Database Tables
```python
Base.metadata.create_all(bind=engine)
```
Automatically creates all tables in the database based on the defined models.

---

# FastAPI & Pydantic Concepts

## 6. `Depends`
- Used in **route functions** to inject dependencies (e.g., database session, authentication).
- **Should NOT be used in normal functions** unless they are dependencies in a FastAPI route.

## 7. `response_model`
- Defines the **response format** for an endpoint, ensuring **consistent API responses**.
- Filters out unwanted fields from database models before returning a response.

## 8. **Pydantic Models**
- Used for **request validation** and **serialization of data**.
- Ensures that incoming data follows the expected format.

## 9. **`BaseModel` in Pydantic**
- The base class for all **Pydantic models**.
- Helps in **data validation and serialization**.

## 10. **`class Config: from_attributes = True`**
```python
class Config:
    from_attributes = True
```
- **Maps SQLAlchemy models to Pydantic models** for easy conversion.
- **If missing**, trying to convert ORM models may result in:
  ```plaintext
  ValueError: UserResponse fields do not match the provided object
  ```

## 11. **`model_validate`**
```python
user_response = UserResponse.model_validate(user)
```
- Converts **database objects (ORM models)** into **Pydantic models** while ensuring validation.

---

# Advanced Concepts

## 12. **ContextVar**
- **Used to store request-specific data** (e.g., storing the current user ID in a global context).
- Helps manage **user authentication state** within a request.

## 13. **SQLAlchemy Event Listeners**
```python
@event.listens_for(Base, 'before_insert', propagate=True)
def before_insert(mapper, connection, target):
    target.created_at = datetime.utcnow()
```
- **`propagate=True`** ensures that the event listener **applies to all subclasses** of `Base`.
- Commonly used for **automatic timestamps (`created_at`, `updated_at`)** and **tracking changes**.

