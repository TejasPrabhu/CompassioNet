import express from 'express';
import * as User from '../models/User';

const router = express.Router();

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

export default router;
