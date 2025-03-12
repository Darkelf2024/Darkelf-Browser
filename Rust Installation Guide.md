# Rust Installation and Project Setup Guide

This guide will walk you through the installation of Rust, setting up a new Rust project, and integrating the `crypto_rust` library with the provided `lib.rs` and `Cargo.toml` files.

## Prerequisites

- Ensure you have `curl` installed.
- Ensure you have `pip` and `virtualenv` installed for Python environment setup.
- Basic knowledge of terminal commands.

## Step 1: Install Rust

1. **Install Rust using `rustup`**:
    ```sh
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

2. **Follow the on-screen instructions** to complete the installation. Once installed, you need to add Rust to your system's `PATH`.

3. **Verify the installation**:
    ```sh
    rustc --version
    ```

## Step 2: Set Up Python Virtual Environment

1. **Create a virtual environment**:
    ```sh
    python3 -m venv ~/pqcrypto_env
    ```

2. **Activate the virtual environment**:
    ```sh
    source ~/pqcrypto_env/bin/activate
    ```

3. **Install Maturin** for building and developing Python extensions in Rust:
    ```sh
    pip install maturin
    ```

## Step 3: Create and Navigate to Rust Project Directory

1. **Navigate to your project directory**:
    ```sh
    cd ~
    mkdir crypto_rust
    cd crypto_rust
    ```

2. **Initialize a new Rust library**:
    ```sh
    cargo new --lib crypto_rust
    cd crypto_rust
    ```

## Step 4: Update `Cargo.toml`

Replace the contents of `Cargo.toml` with the following:

````toml name=crypto_rust/Cargo.toml
[package]
name = "crypto_rust"
version = "0.1.0"
edition = "2021"

[dependencies]
pyo3 = { version = "0.20", features = ["extension-module"] }
rand = "0.8"
x25519-dalek = "2.0"
pqc_kyber = "0.7.1"
sha2 = "0.10"
hkdf = "0.12"
arrayref = "0.3"
aes-gcm = "0.10"
chacha20 = "0.9"
rsa = "0.5"
base64 = "0.13"

[lib]
name = "crypto_rust"
crate-type = ["cdylib"]
