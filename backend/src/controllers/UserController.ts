import express from 'express';
import bcrypt from 'bcrypt';
import { Request as ExpressRequest, Response, NextFunction } from 'express';
import jwt, { JwtPayload } from 'jsonwebtoken';
import * as User from '../models/User';

const router = express.Router();
const JWT_SECRET_KEY = '87e2a3b0e4e729f5d08e2a20f9dab5398a2c8a0a92bc75217f4ab3f2f0748e36'


interface Request extends ExpressRequest {
  user?: JwtPayload;
}

// Middleware to authenticate based on token
import { VerifyErrors } from 'jsonwebtoken'; // Add this import at the top of your file

const authenticate = (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;
    if (authHeader) {
        const token = authHeader.split(' ')[1];
        jwt.verify(token, JWT_SECRET_KEY, (err, user) => {
            if (err) {
                return res.sendStatus(403);
            }
            if (user) {
                req.user = user as JwtPayload;  // If you are sure that 'user' can be cast to JwtPayload
            }
            next();
        });
    } else {
        res.sendStatus(401);
    }
};



// Create User
router.post('/', async (req, res) => {
    try {
        const newUser = await User.create(req.body);
        res.status(201).json(newUser);
    } catch (error: any ) {
        res.status(500).json({ error: error.toString() });
    }
});

// Get all Users
router.get('/', async (_req, res) => {
    try {
        const users = await User.findAll();
        res.json(users);
    } catch (error: any )  {
        res.status(500).json({ error: error.toString() });
    }
});

// Get User by id
router.get('/:id', async (req, res) => {
    try {
        const user = await User.findById(req.params.id);
        if (user) {
            res.json(user);
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    } catch (error: any )  {
        res.status(500).json({ error: error.toString() });
    }
});

// Update User by id
router.put('/:id', async (req, res) => {
    try {
        const updatedUser = await User.update(req.params.id, req.body);
        if (updatedUser) {
            res.json(updatedUser);
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    } catch (error: any )  {
        res.status(500).json({ error: error.toString() });
    }
});

// Delete User by id
router.delete('/:id', async (req, res) => {
    try {
        const deleted = await User.remove(req.params.id);
        if (deleted) {
            res.status(204).end();
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    } catch (error: any )  {
        res.status(500).json({ error: error.toString() });
    }
});



router.post('/login', async (req, res) => {
    const user = await User.findByEmail(req.body.email);
    if (user && await bcrypt.compare(req.body.password, user.password)) {
      const token = jwt.sign({ id: user.id }, JWT_SECRET_KEY, { expiresIn: '1h' });
      res.json({ token });
    } else {
      res.status(401).send('Invalid credentials');
    }
  });



export default router;
