from fastapi import APIRouter, status, HTTPException, Depends, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.depes import get_session


 